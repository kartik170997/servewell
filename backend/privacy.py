"""Local data minimization and deterministic masking; no external detection service."""
import re
from contextlib import contextmanager
from contextvars import ContextVar

PERSONAL_FIELDS = {'submitted_by','contact_phone','store_name','store_address','region_manager',
    'support_phone','user_id','customer_name','full_name','first_name','last_name','email',
    'email_address','phone','phone_number','address','serial_number','preferred_contact','diagnostic_links'}
SECRET_FIELDS = {'api_key','claude_key','pinecone_key','password','secret','authorization','token','app_token','x-api-key'}
CHECKLIST_FIELDS = {'asset_type','error_code','first_occurrence','frequency','affected_devices',
    'affected_users','business_impact','workaround','availability','constraints','steps_already_tried',
    'deadline','prior_troubleshooting_minutes','store_id','asset_id','system_version'}
TICKET_FIELDS = {'ticket_id','store_id','asset_id','system_version','date_opened','priority',
    'category','subcategory','subject','description','tags','status','escalation_flag','procedure_ref','checklist_optional'}
_KNOWN = ContextVar('privacy_known_values',default=())
SECRETS=set()
EMAIL = re.compile(r'(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b')
PHONE = re.compile(r'(?<![\w])(?:\+\d{1,3}[ .-]?)?(?:\(?\d{2,5}\)?[ .-]?){2,5}\d{2,5}(?![\w])')
LABELED = re.compile(r'(?im)\b(my name is|customer name|submitted by|contact name|full name|store address|home address|address)\s*(?:is\s+|[:=]\s*)?([^\n,;.!?]+)')


def as_data(value):
    if isinstance(value,type): return value.__name__
    if hasattr(value,'model_dump'): return value.model_dump(mode='json')
    return value


def known_values(value):
    found=set(_KNOWN.get())|SECRETS
    def walk(v):
        v=as_data(v)
        if isinstance(v,dict):
            for k,x in v.items():
                if str(k).lower() in PERSONAL_FIELDS|SECRET_FIELDS and isinstance(x,str) and len(x.strip())>=3 and x not in ('Not provided','UNSPECIFIED','none'):
                    found.add(x.strip())
                walk(x)
        elif isinstance(v,(list,tuple)):
            for x in v: walk(x)
    walk(value)
    return tuple(sorted(found,key=len,reverse=True))


@contextmanager
def scope(value):
    token=_KNOWN.set(known_values(value))
    try: yield
    finally: _KNOWN.reset(token)


def mask_text(text,known=()):
    for value in known or tuple(sorted(set(_KNOWN.get())|SECRETS,key=len,reverse=True)):
        text=re.sub(r'(?<!\w)'+re.escape(value)+r'(?!\w)','[PRIVATE]',text,flags=re.I)
    text=EMAIL.sub('[EMAIL]',text)
    text=re.sub(r'(?i)\b(contact(?: phone)?|phone(?: number)?|mobile)\s*(?:is\s+|[:=]\s*)?\+?[\d ()-]{5,25}',r'\1 [PHONE]',text)
    def phone(m):
        value=m.group(); digits=re.sub(r'\D','',value)
        # Preserve ISO dates, timestamps and IPv4 addresses used in troubleshooting.
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}',value) or re.fullmatch(r'(?:\d{1,3}\.){3}\d{1,3}',value): return value
        return '[PHONE]' if 10<=len(digits)<=15 else value
    text=PHONE.sub(phone,text)
    text=re.sub(r'(?<!\w)(?:\d[ -]?){15,18}\d(?!\w)','[PRIVATE_NUMBER]',text)
    text=LABELED.sub(lambda m:m[1]+' [PRIVATE]',text)
    text=re.sub(r'(?i)\bBearer\s+[^\s"\']+','Bearer [redacted]',text)
    text=re.sub(r'\bsk-[A-Za-z0-9_-]{12,}','[redacted]',text)
    text=re.sub(r'(?i)\b(api[_ -]?key|password|secret|access[_ -]?token)\s*[:=]\s*[^\s,;]+',r'\1=[redacted]',text)
    # URLs may contain personal identifiers, credentials, or signed query parameters.
    text=re.sub(r'https?://[^\s<>"\']+','[LINK]',text)
    return text


def redact(value,source=None):
    known=known_values(source if source is not None else value)
    def walk(v):
        v=as_data(v)
        if isinstance(v,dict):
            return {k:('[PRIVATE]' if str(k).lower() in PERSONAL_FIELDS and not isinstance(x,bool) else '[redacted]' if str(k).lower() in SECRET_FIELDS else walk(x)) for k,x in v.items()}
        if isinstance(v,(list,tuple)): return [walk(x) for x in v]
        if isinstance(v,str): return mask_text(v,known)
        return v
    return walk(value)


def model_payload(value):
    """Preserve ticket PII for workflow reasoning; strip credentials only."""
    secrets=set(SECRETS)
    def collect(v):
        if isinstance(v,dict):
            for k,x in v.items():
                if str(k).lower() in SECRET_FIELDS and isinstance(x,str) and x: secrets.add(x)
                collect(x)
        elif isinstance(v,(list,tuple)):
            for x in v: collect(x)
    collect(value)
    def walk(v):
        v=as_data(v)
        if isinstance(v,dict): return {k:'[redacted]' if str(k).lower() in SECRET_FIELDS else walk(x) for k,x in v.items()}
        if isinstance(v,(list,tuple)): return [walk(x) for x in v]
        if isinstance(v,str):
            for secret in sorted(secrets,key=len,reverse=True): v=v.replace(secret,'[redacted]')
            v=re.sub(r'(?i)\bBearer\s+[^\s"\']+','Bearer [redacted]',v)
            v=re.sub(r'\bsk-[A-Za-z0-9_-]{12,}','[redacted]',v)
            v=re.sub(r'(?i)\b(api[_ -]?key|password|secret|access[_ -]?token)\s*[:=]\s*[^\s,;]+',r'\1=[redacted]',v)
        return v
    return walk(value)


def ticket_context(t,task='classify'):
    fields=TICKET_FIELDS|PERSONAL_FIELDS|{'asset_details','store_details','escalation_info','ticket_history','resolution_notes'}
    return model_payload({k:t[k] for k in fields if k in t})


def local_contact_updates(text):
    """Capture explicitly labeled contacts locally; ambiguous values stay in the checklist UI."""
    result={}
    name=re.search(r'(?i)\b(?:my name is|customer name\s*[:=]|submitted by\s*[:=])\s*([^\n,;.!?]+)',text)
    if name: result['submitted_by']=name[1].strip()[:200]
    phone=re.search(r'(?i)\b(?:contact(?: phone)?|phone(?: number)?|mobile)\s*(?:is\s+|[:=]\s*)?(\+?[\d ()-]{5,25})',text)
    if phone: result['contact_phone']=phone[1].strip()
    address=re.search(r'(?im)\b(?:store address|address)\s*[:=]\s*([^\n;]+)',text)
    if address: result['store_address']=address[1].strip()
    labels={'customer name':'submitted_by','frequency':'frequency','issue frequency':'frequency',
            'number of affected devices':'affected_devices','affected devices':'affected_devices',
            'affected users':'affected_users','number of affected users':'affected_users',
            'contact method':'preferred_contact','contract metod':'preferred_contact','preferred contact method':'preferred_contact',
            'store address':'store_address','contact phone':'contact_phone','workaround':'workaround',
            'availability':'availability','constraints':'constraints'}
    for line in text.splitlines():
        match=re.match(r'^\s*([a-z ]+)\s*[-:=–]\s*(.+?)\s*$',line,re.I)
        if match:
            label=match[1].strip().casefold().replace('afftected','affected').replace('contrtact','contact').replace('metod','method')
            if label in labels: result[labels[label]]=match[2].strip()
    return result


def scoped(fn):
    import functools
    @functools.wraps(fn)
    def wrapped(*args,**kwargs):
        with scope([args,kwargs]): return fn(*args,**kwargs)
    return wrapped
