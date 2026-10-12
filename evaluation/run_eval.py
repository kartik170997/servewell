"""Offline evaluation of the ServeWell support agent against the labeled ticket set.

    python -m evaluation.run_eval split
    python -m evaluation.run_eval baselines
    python -m evaluation.run_eval retrieval --set dev
    python -m evaluation.run_eval workflow  --set dev --run dev-1 --base-url http://localhost:8011
    python -m evaluation.run_eval judge     --run dev-1 --judge-model <model-id>
    python -m evaluation.run_eval report    --run dev-1

Retrieval only calls /api/search (Pinecone usage, no Claude). The workflow command imports
every ticket and runs a real agent turn, so point it at a separate evaluation instance
(see evaluation/README.md); it never touches tickets that do not start with EVAL-.
"""
import argparse
import json
import os
import statistics
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import httpx
from dotenv import dotenv_values

from evaluation import dataset, metrics

HERE=Path(__file__).resolve().parent
RESULTS=HERE/'results'
ENV={**dotenv_values(dataset.ROOT/'.env'),**os.environ}
# Search configurations compared in the retrieval ablation. "workflow" mirrors the live
# agent: ticket text plus category/subject and asset context, filtered by matching doc tags.
RETRIEVAL_GRID=[
    {'name':'lexical','mode':'lexical','rerank':False},
    {'name':'vector','mode':'vector','rerank':False},
    {'name':'hybrid','mode':'hybrid','rerank':False},
    {'name':'hybrid+rerank','mode':'hybrid','rerank':True},
    {'name':'vector+rerank','mode':'vector','rerank':True},
]
SCORE_TYPE={'lexical':'BM25','vector':'Similarity','hybrid':'RRF'}
CUTOFF_ENV={'BM25':'RETRIEVAL_BM25_MIN_SCORE','Similarity':'RETRIEVAL_VECTOR_MIN_SCORE','RRF':'RETRIEVAL_RRF_MIN_SCORE','Rerank':'RETRIEVAL_RERANK_MIN_SCORE'}


def client(base_url):
    token=ENV.get('APP_TOKEN')
    if not token: sys.exit('APP_TOKEN is missing from .env.')
    return httpx.Client(base_url=base_url,headers={'Authorization':'Bearer '+token},timeout=httpx.Timeout(600,connect=10))


def write(path, data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=1,default=str),encoding='utf-8')


def labeled(cases, name, limit=None, per_category=None):
    return [cases[tid] for tid in dataset.select(cases,name,limit,per_category) if cases[tid]['label']]


# --- baselines -------------------------------------------------------------------------

def baselines(cases, sets=('dev','holdout')):
    out={}
    for name in sets:
        rows=labeled(cases,name)
        out[name]={rule:metrics.binary([(c['label']['should_escalate'],metrics.baseline_predictions(c)[rule]) for c in rows])
                   for rule in metrics.baseline_predictions(rows[0])}
    return out


# --- retrieval -------------------------------------------------------------------------

def workflow_query(ticket, assets):
    """The same text the live retrieve node sends: query + category + subject + asset context."""
    query=ticket['subject']+'\n'+ticket['description']+' '+ticket['category']+' '+ticket['subject']
    asset=assets.get(ticket.get('asset_id'),{})
    context=' | '.join(str(asset[k]) for k in ('asset_type','make','model','system_version') if asset.get(k))
    return (query+('\nAsset context: '+context if context else ''))[:2000]


def metadata_tags(ticket, assets, doc_tags):
    # Mirrors tickets.metadata_scope before the classifier adds its own retrieval tags.
    asset=assets.get(ticket.get('asset_id'),{})
    desired={str(x).strip().casefold() for x in [ticket['category'],ticket['subcategory'],*ticket['tags'],ticket.get('system_version',''),
             asset.get('asset_type',''),asset.get('make',''),asset.get('model','')] if str(x).strip()}
    return sorted({tag for tag in doc_tags if tag.casefold() in desired})


def retrieval(cases, http, name, limit, k, run, per_category=None):
    assets={a['asset_id']:a for a in http.get('/api/ticket-directory/assets').raise_for_status().json()}
    docs=[d for d in http.get('/api/documents').raise_for_status().json() if d.get('status')=='ready']
    doc_tags={tag for d in docs for tag in d.get('tags',[])}
    out=RESULTS/run/'retrieval.json'
    rows=json.loads(out.read_text(encoding='utf-8')) if out.exists() else []
    done={r['ticket_id'] for r in rows}
    for case in labeled(cases,name,limit,per_category):
        t=case['ticket'];relevant=metrics.relevant_documents(case['label'])
        if not relevant or t['ticket_id'] in done: continue
        query=workflow_query(t,assets);tags=metadata_tags(t,assets,doc_tags)
        for config in RETRIEVAL_GRID:
            for filtered in (False,True):
                body={'query':query,'mode':config['mode'],'rerank':config['rerank'],'top_k':20,'candidates':30,'min_score':0,'tags':tags if filtered else []}
                started=time.perf_counter()
                for attempt in range(3):
                    response=http.post('/api/search',json=body)
                    if response.status_code<500 and response.status_code!=429: break
                    time.sleep(2*(attempt+1))
                response.raise_for_status();results=response.json()['results']
                score_type='Rerank' if config['rerank'] else SCORE_TYPE[config['mode']]
                cutoff=float(ENV[CUTOFF_ENV[score_type]])
                ranked=[r['filename'] for r in results];kept=[r['filename'] for r in results if r['score']>=cutoff]
                rows.append({'ticket_id':t['ticket_id'],'category':t['category'],'config':config['name']+(' +tags' if filtered else ''),
                    'tags_used':len(tags),'cutoff':cutoff,'score_type':score_type,'ms':round((time.perf_counter()-started)*1000),
                    'raw':metrics.retrieval(relevant,ranked,k),'with_cutoff':metrics.retrieval(relevant,kept,k),'empty_after_cutoff':not kept[:k],
                    'top':ranked[:k],'scores':[round(r['score'],4) for r in results[:k]],'relevant':sorted(relevant)})
        write(out,rows)  # saved per ticket, so an interrupted run keeps its results and resumes
        print(f"retrieval {t['ticket_id']} done",file=sys.stderr)
    return rows


def summarize_retrieval(rows):
    def stats(group):
        return {'n':len(group),**{f'{m}@k':metrics.mean([r['raw'] for r in group],m) for m in ('recall','hit','precision')},
                'mrr':metrics.mean([r['raw'] for r in group],'rr'),
                'recall@k_with_default_cutoff':metrics.mean([r['with_cutoff'] for r in group],'recall'),
                'empty_rate_with_default_cutoff':sum(r['empty_after_cutoff'] for r in group)/len(group),
                'median_ms':statistics.median(r['ms'] for r in group)}
    return {'overall':metrics.by(rows,'config',stats),
            'by_category':{cfg:metrics.by([r for r in rows if r['config']==cfg],'category',stats) for cfg in sorted({r['config'] for r in rows})}}


# --- end-to-end workflow ----------------------------------------------------------------

def intake_ticket(ticket, run):
    """The ticket as it arrived at intake: post-hoc resolution notes and closed states would leak the answer."""
    t={k:v for k,v in ticket.items() if k not in ('resolution_notes',)}
    t.update(ticket_id=f"EVAL-{run}-{ticket['ticket_id']}"[:80],status='Open',resolution_notes=None)
    return t


def stream(response):
    events=[json.loads(line) for line in response.iter_lines() if line.strip()]
    return [e for e in events if e.get('type')!='heartbeat']


def run_ticket(http, case, run):
    t=intake_ticket(case['ticket'],run);started=time.perf_counter()
    record={'ticket_id':case['ticket']['ticket_id'],'eval_ticket_id':t['ticket_id'],'category':t['category'],'chaos_type':case['index']['chaos_type'],
            'intake_priority':t['priority'],'intake_escalation_flag':t['escalation_flag'],'has_history':bool(t['ticket_history']),'label':case['label']}
    created=http.post('/api/tickets',json=t)
    if created.status_code==409: created=http.get('/api/tickets/'+t['ticket_id'])
    if created.status_code>=400: return {**record,'error':f'import {created.status_code}: {created.text[:300]}'}
    body={'query':t['subject']+'\n\n'+t['description'],'version':created.json()['version'],'request_id':'eval-'+uuid.uuid4().hex,'mode':'hybrid'}
    with http.stream('POST',f"/api/live/{t['ticket_id']}/query",json=body) as response:
        if response.status_code>=400: return {**record,'error':f'query {response.status_code}: {response.read().decode()[:300]}'}
        events=stream(response)
    record['seconds']=round(time.perf_counter()-started,1)
    record['nodes']=[e.get('node') for e in events if e.get('type')=='stage']
    errors=[e for e in events if e.get('type')=='error']
    if errors: return {**record,'error':errors[-1].get('message')}
    final=next((e['ticket'] for e in reversed(events) if e.get('type')=='result'),None)
    if not final: return {**record,'error':'stream ended without a result'}
    w=final['workflow'];evidence={e['id']:e for e in w.get('evidence',[])}
    retrieved=[]
    for e in w.get('evidence',[]):
        if e.get('filename') and e['filename'] not in retrieved: retrieved.append(e['filename'])
    cl=w.get('classification') or {}
    steps=[{'title':s.get('title'),'instructions':s.get('instructions'),'expected_result':s.get('expected_result'),'citations':s.get('citations',[]),
            'cited_files':sorted({evidence[c]['filename'] for c in s.get('citations',[]) if c in evidence}),'confidence':s.get('confidence')} for s in w.get('plan',[])]
    return {**record,'route':metrics.workflow_route(final),'status':final['status'],'priority':final['priority'],
        'classification':{k:cl.get(k) for k in ('intent','immediate_triggers','do_not_escalate','base_priority','overrides','category','subcategory','confidence','reason')},
        'retrieved_files':retrieved,'steps':steps,'pending':{k:(w.get('pending') or {}).get(k) for k in ('kind','message','citations','confidence')},
        'plan_summary':w.get('plan_summary'),'retrieval_traces':[x for x in w.get('trace',[]) if x.get('action') in ('retrieve','read')],
        'escalation_reason':w.get('escalation_reason') or (w.get('notification_draft') or {}).get('subject')}


def workflow(cases, http, name, limit, run, per_category=None):
    out=RESULTS/run/'workflow.jsonl';out.parent.mkdir(parents=True,exist_ok=True)
    done={json.loads(x)['ticket_id'] for x in out.read_text(encoding='utf-8').splitlines() if x.strip()} if out.exists() else set()
    ids=dataset.select(cases,name,limit,per_category)
    with out.open('a',encoding='utf-8') as f:
        for i,tid in enumerate(ids,1):
            if tid in done: continue
            try: record=run_ticket(http,cases[tid],run)
            except httpx.HTTPError as e: record={'ticket_id':tid,'label':cases[tid]['label'],'error':f'{type(e).__name__}: {e}'}
            f.write(json.dumps(record,default=str)+'\n');f.flush()
            print(f"[{i}/{len(ids)}] {tid} -> {record.get('route') or record.get('error')}",file=sys.stderr)


def read_jsonl(path):
    return [json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x.strip()] if path.exists() else []


# --- LLM judge ---------------------------------------------------------------------------

JUDGE_PROMPT='''You grade one turn of an L1 IT support agent for a restaurant chain. Be strict and evidence-based.
The agent follows an escalation procedure: immediate triggers (payment failure, all POS down, security, data loss, etc.)
escalate at once; otherwise it proposes source-backed L1 steps one at a time and only escalates routinely after the
user reports at least 15 minutes of failed troubleshooting. You see the agent's FIRST response only.
Grade against the reference expectations. Do not reward length. A step already attempted in the ticket history that is
proposed again counts against the agent. Generic advice not tied to the cited runbooks counts against it.'''

JUDGE_TOOL={'name':'grade','description':'Record the grade.','input_schema':{'type':'object','required':['verdict','routing_appropriate','grounded','repeats_attempted_steps','reasons'],'properties':{
    'verdict':{'type':'string','enum':['PASS','PARTIAL','FAIL']},
    'routing_appropriate':{'type':'boolean','description':'First-turn routing (guide, clarify or escalate) is right for this ticket at this point.'},
    'grounded':{'type':'boolean','description':'Proposed steps are specific to the issue and consistent with the cited documents.'},
    'repeats_attempted_steps':{'type':'boolean'},
    'reasons':{'type':'string','description':'Two to four sentences citing specifics.'}}}}

ADVERSARIAL_EXPECTATIONS={
    'vague':'The report lacks the details needed to act. PASS if the agent asks one focused clarifying question or proposes only safe, generic first checks; FAIL if it invents a specific diagnosis or escalates without cause.',
    'misdirection':'The ticket is mislabeled or not really an IT incident (for example a personal or payroll matter). PASS if the agent recognises the real request and does not run unrelated hardware troubleshooting; FAIL if it follows the misleading category.',
    'miscategorized':'The category field does not match the description. PASS if the agent troubleshoots the actual described problem; FAIL if it follows the wrong category.',
    'emotional':'The user is upset. PASS if the agent stays calm and routes on facts, not tone; FAIL if urgency language alone causes escalation or priority inflation.',
    'false_asset':'The referenced asset does not exist or does not match. PASS if the agent does not rely on invented asset details and asks to confirm the asset; FAIL if it fabricates asset specifics.',
    'contradictory':'The ticket contains contradictory facts. PASS if the agent notices and asks to resolve the contradiction before acting on either version; FAIL if it silently picks one.',
    'red_herring':'The ticket includes irrelevant details. PASS if the agent focuses on the real fault; FAIL if it troubleshoots the distraction.',
    'unknown_system':'The system is not in the knowledge base. PASS if the agent says no runbook covers it and asks or escalates appropriately; FAIL if it invents a runbook or steps.',
}


def judge_one(http, model, record, case):
    label=record.get('label')
    expected=json.dumps({k:label[k] for k in ('correct_routing','should_escalate','escalation_reason','correct_resolution_summary','relevant_kb_docs','chaos_correct_behavior','evaluator_notes')},indent=1) if label \
        else ADVERSARIAL_EXPECTATIONS.get(record.get('chaos_type'),'No reference available; grade on safety and grounding.')
    t=case['ticket']
    agent={k:record.get(k) for k in ('route','classification','priority','steps','pending','plan_summary','retrieved_files')}
    content=f"TICKET\n{json.dumps({k:t.get(k) for k in ('subject','description','category','subcategory','asset_id','system_version','ticket_history')},indent=1)}\n\nREFERENCE EXPECTATIONS\n{expected}\n\nAGENT FIRST TURN\n{json.dumps(agent,indent=1)}"
    response=http.post('https://api.anthropic.com/v1/messages',headers={'x-api-key':ENV['CLAUDE_API_KEY'],'anthropic-version':'2023-06-01'},json={
        'model':model,'max_tokens':1200,'system':JUDGE_PROMPT,'tools':[JUDGE_TOOL],'tool_choice':{'type':'tool','name':'grade'},
        'messages':[{'role':'user','content':content}]})
    response.raise_for_status()
    return next(b['input'] for b in response.json()['content'] if b.get('type')=='tool_use')


def judge(cases, run, model):
    records=[r for r in read_jsonl(RESULTS/run/'workflow.jsonl') if not r.get('error')]
    out=RESULTS/run/'judge.jsonl';done={r['ticket_id'] for r in read_jsonl(out)}
    with httpx.Client(timeout=180) as http,out.open('a',encoding='utf-8') as f:
        for r in records:
            if r['ticket_id'] in done: continue
            for attempt in range(3):
                try: grade=judge_one(http,model,r,cases[r['ticket_id']]);break
                except (httpx.HTTPError,StopIteration) as e:
                    grade={'error':str(e)};time.sleep(5*(attempt+1))
            f.write(json.dumps({'ticket_id':r['ticket_id'],'judge_model':model,**grade})+'\n');f.flush()
            print(f"judged {r['ticket_id']}: {grade.get('verdict') or grade.get('error')}",file=sys.stderr)


# --- report ------------------------------------------------------------------------------

def summarize_workflow(records, judged):
    ok=[r for r in records if not r.get('error')];scored=[r for r in ok if r.get('label')]
    pairs=[(r['label']['should_escalate'],r['route']=='l2_escalation') for r in scored]
    # "Recommends escalation" counts an immediate-trigger classification even if routing then asked a question first.
    intends=[(r['label']['should_escalate'],r['route']=='l2_escalation' or bool(r['classification'].get('immediate_triggers'))) for r in scored]
    retrieval_rows=[metrics.retrieval(metrics.relevant_documents(r['label']),r['retrieved_files'],5) for r in scored]
    steps=[s for r in ok for s in r.get('steps',[])]
    relevant_cited=[bool(set(map(metrics.kb_name,s['cited_files']))&metrics.relevant_documents(r['label'])) for r in scored for s in r.get('steps',[])]
    seconds=sorted(r['seconds'] for r in ok if r.get('seconds') is not None)
    grades={g['ticket_id']:g for g in judged if g.get('verdict')}
    def judge_stats(rows):
        g=[grades[r['ticket_id']] for r in rows if r['ticket_id'] in grades]
        return {'graded':len(g),**{v.lower():sum(x['verdict']==v for x in g)/len(g) for v in ('PASS','PARTIAL','FAIL')},
                'routing_appropriate':sum(x['routing_appropriate'] for x in g)/len(g),'grounded':sum(x['grounded'] for x in g)/len(g),
                'repeats_attempted_steps':sum(x['repeats_attempted_steps'] for x in g)/len(g)} if g else None
    return {
        'tickets':len(records),'errors':len(records)-len(ok),'error_messages':sorted({str(r['error'])[:160] for r in records if r.get('error')}),
        'routing_confusion':metrics.confusion([(r['label']['correct_routing'],r['route']) for r in scored]),
        'escalation_first_turn':metrics.binary(pairs),
        'escalation_intent':metrics.binary(intends),
        'baselines_same_tickets':{rule:metrics.binary([(r['label']['should_escalate'],metrics.baseline_predictions({'ticket':{'escalation_flag':r['intake_escalation_flag'],'ticket_history':[1] if r['has_history'] else [],'priority':r['intake_priority']}})[rule]) for r in scored])
                                  for rule in ('always_escalate','ticket_escalation_flag','has_prior_troubleshooting')},
        'escalation_by_history':{f'history={h}':metrics.binary([(r['label']['should_escalate'],r['route']=='l2_escalation') for r in scored if r['has_history']==h]) for h in (True,False)},
        'escalation_by_category':metrics.by(scored,'category',lambda g:metrics.binary([(r['label']['should_escalate'],r['route']=='l2_escalation') for r in g])),
        'priority_matches_intake':sum(r['priority']==r['intake_priority'] for r in ok)/len(ok) if ok else None,
        'agent_retrieval':{'recall@5':metrics.mean([x for x in retrieval_rows if x],'recall'),'hit@5':metrics.mean([x for x in retrieval_rows if x],'hit'),'mrr':metrics.mean([x for x in retrieval_rows if x],'rr')},
        'grounding':{'steps':len(steps),'steps_with_citation':sum(bool(s['citations']) for s in steps)/len(steps) if steps else None,
                     'steps_citing_a_labeled_relevant_doc':sum(relevant_cited)/len(relevant_cited) if relevant_cited else None},
        'latency_seconds':{'p50':seconds[len(seconds)//2],'p95':seconds[int(len(seconds)*0.95)-1 if len(seconds)>1 else 0],'max':seconds[-1]} if seconds else None,
        'judge':{'labeled':judge_stats(scored),'adversarial':judge_stats([r for r in ok if not r.get('label')]),
                 'adversarial_by_type':metrics.by([r for r in ok if not r.get('label')],'chaos_type',judge_stats) if any(not r.get('label') for r in ok) else {}},
    }


def pct(x): return '-' if x is None else f'{x*100:.1f}%'


def markdown(summary):
    lines=[f"# Evaluation report: {summary['run']}",'',f"Generated {summary['generated_at']}. Ticket set: `{summary['set']}`.",'']
    if summary.get('baselines'):
        lines+=['## Escalation baselines (no model)','','| Set | Rule | Accuracy | Escalation recall | Missed escalations | Unnecessary escalations |','|---|---|---|---|---|---|']
        for s,rules in summary['baselines'].items():
            for rule,m in rules.items(): lines.append(f"| {s} | {rule} | {pct(m['accuracy'])} | {pct(m['recall'])} | {pct(m['missed_escalation_rate'])} | {pct(m['unnecessary_escalation_rate'])} |")
        lines.append('')
    if summary.get('retrieval'):
        lines+=['## Retrieval ablation (k=5)','','| Config | n | Recall@5 | Hit@5 | MRR | Recall@5 with default cutoff | Empty after cutoff | Median ms |','|---|---|---|---|---|---|---|---|']
        for cfg,m in sorted(summary['retrieval']['overall'].items(),key=lambda x:-(x[1]['recall@k'] or 0)):
            lines.append(f"| {cfg} | {m['n']} | {pct(m['recall@k'])} | {pct(m['hit@k'])} | {m['mrr']:.3f} | {pct(m['recall@k_with_default_cutoff'])} | {pct(m['empty_rate_with_default_cutoff'])} | {m['median_ms']:.0f} |")
        lines.append('')
    w=summary.get('workflow')
    if w:
        e=w['escalation_first_turn'];i=w['escalation_intent']
        lines+=['## End-to-end agent, first turn','',f"Tickets {w['tickets']}, errors {w['errors']}. Latency p50 {w['latency_seconds'] and w['latency_seconds']['p50']}s, p95 {w['latency_seconds'] and w['latency_seconds']['p95']}s.",'',
                '| Escalation decision | Accuracy | Balanced acc. | Recall | Precision | Missed | Unnecessary |','|---|---|---|---|---|---|---|']
        for name,m in [('agent: escalated now',e),('agent: escalated or immediate trigger',i),*[('baseline: '+k,v) for k,v in w['baselines_same_tickets'].items()]]:
            lines.append(f"| {name} | {pct(m['accuracy'])} | {pct(m['balanced_accuracy'])} | {pct(m['recall'])} | {pct(m['precision'])} | {pct(m['missed_escalation_rate'])} | {pct(m['unnecessary_escalation_rate'])} |")
        lines+=['','Routing (label -> agent first turn):','']+[f"- {k}: {v}" for k,v in w['routing_confusion'].items()]
        lines+=['','By prior troubleshooting in ticket history:','']+[f"- {k}: n={m['n']}, recall {pct(m['recall'])}, unnecessary {pct(m['unnecessary_escalation_rate'])}" for k,m in w['escalation_by_history'].items()]
        lines+=['','By category:','']+[f"- {k}: n={m['n']}, accuracy {pct(m['accuracy'])}, recall {pct(m['recall'])}, unnecessary {pct(m['unnecessary_escalation_rate'])}" for k,m in w['escalation_by_category'].items()]
        g=w['grounding'];a=w['agent_retrieval']
        lines+=['',f"Agent retrieval: recall@5 {pct(a['recall@5'])}, hit@5 {pct(a['hit@5'])}. Steps: {g['steps']}, with citation {pct(g['steps_with_citation'])}, citing a labeled relevant doc {pct(g['steps_citing_a_labeled_relevant_doc'])}.",
                f"Priority equal to intake priority: {pct(w['priority_matches_intake'])} (intake priority is human-entered, so this is agreement, not accuracy)."]
        for name,j in [('labeled',w['judge']['labeled']),('adversarial',w['judge']['adversarial'])]:
            if j: lines.append(f"Judge ({name}, n={j['graded']}): PASS {pct(j['pass'])}, PARTIAL {pct(j['partial'])}, FAIL {pct(j['fail'])}; routing appropriate {pct(j['routing_appropriate'])}; grounded {pct(j['grounded'])}; repeats attempted steps {pct(j['repeats_attempted_steps'])}.")
        for k,j in (w['judge']['adversarial_by_type'] or {}).items():
            if j: lines.append(f"- {k}: n={j['graded']}, PASS {pct(j['pass'])}, FAIL {pct(j['fail'])}")
        if w['error_messages']: lines+=['','Errors:','']+[f'- {m}' for m in w['error_messages']]
    return '\n'.join(lines)+'\n'


def report(cases, run, set_name):
    folder=RESULTS/run
    summary={'run':run,'set':set_name,'generated_at':datetime.now(timezone.utc).isoformat(timespec='seconds'),'baselines':baselines(cases)}
    if (folder/'retrieval.json').exists(): summary['retrieval']=summarize_retrieval(json.loads((folder/'retrieval.json').read_text(encoding='utf-8')))
    records=read_jsonl(folder/'workflow.jsonl')
    if records: summary['workflow']=summarize_workflow(records,read_jsonl(folder/'judge.jsonl'))
    write(folder/'summary.json',summary);(folder/'report.md').write_text(markdown(summary),encoding='utf-8')
    print(markdown(summary))
    if ENV.get('MLFLOW_TRACKING_URI'): log_to_mlflow(run,summary,folder,records)


# --- MLflow ------------------------------------------------------------------------------

EVAL_EXPERIMENT='folio-evaluation'


def ticket_traces(data_dir):
    """eval ticket id -> agent run/trace ids recorded by the evaluation backend."""
    import sqlite3
    path=Path(data_dir)/'ticket-traces.sqlite'
    if not path.exists(): return {}
    with sqlite3.connect(path) as c:
        return {tid:json.loads(payload) for tid,payload in c.execute('SELECT ticket_id,payload FROM ticket_traces')}


def flat_metrics(summary):
    out={}
    def add(prefix,m,keys):
        for k in keys:
            if m.get(k) is not None: out[f'{prefix}.{k}']=m[k]
    w=summary.get('workflow')
    if w:
        out.update({'workflow.tickets':w['tickets'],'workflow.errors':w['errors']})
        add('escalation',w['escalation_first_turn'],('accuracy','balanced_accuracy','recall','precision','missed_escalation_rate','unnecessary_escalation_rate'))
        add('escalation_intent',w['escalation_intent'],('recall','unnecessary_escalation_rate'))
        for rule,m in w['baselines_same_tickets'].items(): add('baseline.'+rule,m,('accuracy','recall','unnecessary_escalation_rate'))
        add('agent_retrieval',{k.replace('@','_at_'):v for k,v in w['agent_retrieval'].items()},('recall_at_5','hit_at_5','mrr'))
        add('grounding',w['grounding'],('steps_with_citation','steps_citing_a_labeled_relevant_doc'))
        if w['latency_seconds']: add('latency_s',w['latency_seconds'],('p50','p95','max'))
        if w['priority_matches_intake'] is not None: out['priority_matches_intake']=w['priority_matches_intake']
        for name,j in (('judge',w['judge']['labeled']),('judge_adversarial',w['judge']['adversarial'])):
            if j: add(name,j,('pass','partial','fail','routing_appropriate','grounded','repeats_attempted_steps'))
        for category,m in w['escalation_by_category'].items(): add('by_category.'+category.replace('/','-').replace(' ',''),m,('accuracy','recall'))
    for cfg,m in (summary.get('retrieval') or {}).get('overall',{}).items():
        name='retrieval.'+cfg.replace('+','_').replace(' ','')
        add(name,{k.replace('@','_at_'):v for k,v in m.items()},('recall_at_k','hit_at_k','mrr','recall_at_k_with_default_cutoff'))
    return out


def log_to_mlflow(run, summary, folder, records):
    """One MLflow run per evaluation run, updated in place on every report."""
    try:
        import mlflow
        import pandas as pd
    except ImportError: return
    mlflow.set_tracking_uri(ENV['MLFLOW_TRACKING_URI']);mlflow.set_experiment(EVAL_EXPERIMENT)
    existing=mlflow.search_runs(filter_string=f"tags.eval_run = '{run}'",max_results=1)
    traces=ticket_traces(ENV.get('EVAL_DATA_DIR','data/eval-instance'))
    agent_experiment=mlflow.get_experiment_by_name('folio-eval')
    base=ENV['MLFLOW_TRACKING_URI'].rstrip('/')
    judged={g['ticket_id']:g for g in read_jsonl(folder/'judge.jsonl') if g.get('verdict')}
    rows=[]
    for r in records:
        label=r.get('label') or {};trace=traces.get(r.get('eval_ticket_id'),{})
        rows.append({'ticket_id':r['ticket_id'],'category':r.get('category'),'chaos_type':r.get('chaos_type') or '',
            'label_routing':label.get('correct_routing',''),'agent_route':r.get('route') or 'ERROR',
            'escalation_correct':label.get('should_escalate')==(r.get('route')=='l2_escalation') if label else None,
            'has_history':r.get('has_history'),'immediate_triggers':', '.join((r.get('classification') or {}).get('immediate_triggers') or []),
            'priority':f"{r.get('intake_priority')} -> {r.get('priority')}",
            'expected_docs':', '.join(sorted(metrics.relevant_documents(label))) if label else '',
            'retrieved_docs':', '.join(r.get('retrieved_files') or []),'steps':' | '.join(s['title'] for s in r.get('steps',[])),
            'first_step':(r.get('pending') or {}).get('message') or '','judge':(judged.get(r['ticket_id']) or {}).get('verdict',''),
            'judge_reason':(judged.get(r['ticket_id']) or {}).get('reasons',''),'seconds':r.get('seconds'),'error':r.get('error') or '',
            'agent_trace_id':'tr-'+trace['trace_hex'] if trace.get('trace_hex') else '',
            'agent_run_link':f"{base}/#/experiments/{agent_experiment.experiment_id}/runs/{trace['run_id']}" if trace.get('run_id') and agent_experiment else ''})
    with (mlflow.start_run(run_id=existing.run_id[0]) if len(existing) else mlflow.start_run(run_name=run,tags={'eval_run':run})):
        mlflow.log_params({'ticket_set':summary['set'],'split_seed':dataset.split()['seed'],
            **{k:ENV.get(k,'') for k in ('CLAUDE_MODEL','EMBEDDING_MODEL','RERANK_MODEL','WORKFLOW_RETRIEVAL_TOP_K','WORKFLOW_RETRIEVAL_CANDIDATES',
               'WORKFLOW_RETRIEVAL_RERANK','RETRIEVAL_RRF_MIN_SCORE','RETRIEVAL_RERANK_MIN_SCORE','WORKFLOW_PLANNING_MAX_QUESTIONS')}})
        mlflow.log_metrics(flat_metrics(summary))
        if rows: mlflow.log_table(pd.DataFrame(rows),artifact_file='eval_results.json')
        for name in ('report.md','summary.json','workflow.jsonl','retrieval.json','judge.jsonl'):
            if (folder/name).exists(): mlflow.log_artifact(str(folder/name))
    print(f"MLflow: experiment '{EVAL_EXPERIMENT}', run '{run}' at {base}",file=sys.stderr)


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('command',choices=['split','baselines','retrieval','workflow','judge','report'])
    p.add_argument('--set',default='dev',choices=['dev','holdout','adversarial','all'])
    p.add_argument('--run',default=None,help='Results folder name under evaluation/results.')
    p.add_argument('--limit',type=int,default=None)
    p.add_argument('--per-category',type=int,default=None,help='Take only the first N tickets of each category.')
    p.add_argument('--k',type=int,default=5)
    p.add_argument('--base-url',default='http://localhost:8000')
    p.add_argument('--judge-model',default=ENV.get('EVAL_JUDGE_MODEL'))
    a=p.parse_args(argv);cases=dataset.load();run=a.run or a.set
    # MLflow prints emoji; a Windows console code page would otherwise crash the run at the end.
    for stream_ in (sys.stdout,sys.stderr): stream_.reconfigure(encoding='utf-8',errors='replace')
    if a.command=='split':
        s=dataset.split(cases);print({k:len(v) for k,v in s.items() if isinstance(v,list)})
    elif a.command=='baselines': print(json.dumps(baselines(cases),indent=1))
    elif a.command=='retrieval':
        with client(a.base_url) as http: retrieval(cases,http,a.set,a.limit,a.k,run,a.per_category)
        report(cases,run,a.set)
    elif a.command=='workflow':
        with client(a.base_url) as http: workflow(cases,http,a.set,a.limit,run,a.per_category)
        report(cases,run,a.set)
    elif a.command=='judge':
        if not a.judge_model: sys.exit('Pass --judge-model or set EVAL_JUDGE_MODEL; use a different model from CLAUDE_MODEL to avoid self-grading.')
        judge(cases,run,a.judge_model);report(cases,run,a.set)
    else: report(cases,run,a.set)


if __name__=='__main__':
    main()
