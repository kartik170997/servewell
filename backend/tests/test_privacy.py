import json
import httpx
from dspy.utils import DummyLM
import dspy
import privacy
import live_workflow as L
from test_api import client, providers, configure, main
from test_tickets import ticket, classification
from test_live_workflow import live, start, final, feedback


def test_ticket_context_restores_store_contacts_and_history(client):
    t=ticket(client,description='Maria Chen reports code E42 at 10.0.0.1',
             escalation_info={'store_address':'19 Private Lane','business_impact':'Maria Chen cannot print'})
    t['asset_details']={'model':'POS X','serial_number':'PRIVATE-SERIAL'}
    t['ticket_history']=[{'actor':'Maria Chen','note':'Earlier customer feedback'}]
    t['api_key']='not-for-the-model'
    for task in ('classify','plan','feedback','information'):
        context=privacy.ticket_context(t,task)
        assert context['submitted_by']=='Maria Chen'
        assert context['store_name']==t['store_name']
        assert context['contact_phone']==t['contact_phone']
        assert context['escalation_info']['store_address']=='19 Private Lane'
        assert context['ticket_history']==t['ticket_history']
        assert 'not-for-the-model' not in json.dumps(context)
        assert 'question_history' not in context


def test_dspy_outbound_prompt_preserves_query_evidence_and_contact_fields(client,monkeypatch):
    configure(client)
    captured={}
    class InspectLM(DummyLM):
        def __call__(self,*args,**kwargs):
            captured.update(kwargs)
            return super().__call__(*args,**kwargs)
    lm=InspectLM([{'classification':classification()}],adapter=dspy.JSONAdapter())
    monkeypatch.setattr(dspy,'LM',lambda *a,**kw:lm)
    raw={'submitted_by':'Maria Chen','contact_phone':'+91-98765-43210'}
    with privacy.scope(raw):
        L.predict(L.classify_signature(),'classification',{'query':'Maria Chen: email maria@example.com, phone +91-98765-43210. Printer E42.',
            'evidence':[{'text':'Maria Chen owns the printer.'}]})
    wire=json.dumps(captured['messages'])
    assert all(v in wire for v in ('Maria Chen','maria@example.com','98765'))
    assert 'E42' in wire


def test_provider_boundary_masks_without_modifying_auth(monkeypatch):
    captured={}
    def send(self,method,url,headers,**kwargs):
        captured.update(headers=headers,body=kwargs['json'])
        return httpx.Response(200,json={'ok':True})
    monkeypatch.setattr(httpx.Client,'request',send)
    main.request('POST','https://api.anthropic.com/v1/messages',{'x-api-key':'real-auth'},json={
        'messages':[{'role':'user','content':'My name is Jane Doe. Email jane@example.com. Phone 12345. password=abc123'}]})
    wire=json.dumps(captured['body'])
    assert all(v not in wire for v in ('Jane Doe','jane@example.com','12345','abc123'))
    assert captured['headers']['x-api-key']=='real-auth'


def test_logging_masks_nested_and_repeated_values():
    raw={'ticket':{'submitted_by':'Maria Chen','contact_phone':'12345','store_address':'19 Private Lane'},
         'query':'Maria Chen at 19 Private Lane, phone 12345; email maria@example.com'}
    clean=json.dumps(main.observability.sanitize(raw))
    assert all(v not in clean for v in ('Maria Chen','19 Private Lane','12345','maria@example.com'))
    assert raw['ticket']['submitted_by']=='Maria Chen'


def test_local_contacts_are_saved_without_model_personal_updates(client,live):
    t=final(start(client))
    t=final(feedback(client,t,note='My name is Jane Doe. Phone: +91-98765-43210. Printer is still offline.'))
    assert t['submitted_by']=='Jane Doe'
    assert t['contact_phone']=='+91-98765-43210'
    assert client.get('/api/tickets/'+t['ticket_id']).json()['contact_phone']=='+91-98765-43210'


def test_request_scopes_do_not_leak_to_other_tickets():
    with privacy.scope({'submitted_by':'Alice Smith'}):
        assert 'Alice Smith' not in privacy.mask_text('Alice Smith reports E42')
    assert privacy.mask_text('Alice Smith reports E42')=='Alice Smith reports E42'


def test_workflow_payload_preserves_pii_but_masks_credentials():
    raw={'submitted_by':'Maria Chen','api_key':'secret-key-value',
         'query':'Maria Chen phone +91-98765-43210 password=abc123 secret-key-value'}
    clean=privacy.model_payload(raw)
    assert clean['submitted_by']=='Maria Chen'
    assert '+91-98765-43210' in clean['query']
    assert 'abc123' not in str(clean) and 'secret-key-value' not in str(clean)
    assert raw['api_key']=='secret-key-value'
