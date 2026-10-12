"""Durable ticket-to-trace identity with MLflow distributed child spans."""
import json
import sqlite3
import time
import uuid
from pathlib import Path

DATA = Path('data')


def initialize(data):
    global DATA
    DATA = Path(data)
    with connection() as c:
        c.execute('''CREATE TABLE IF NOT EXISTS ticket_traces (
            destination TEXT, ticket_id TEXT, payload TEXT NOT NULL,
            PRIMARY KEY(destination,ticket_id))''')


def connection():
    return sqlite3.connect(DATA/'ticket-traces.sqlite', timeout=30)


def begin(o, ticket_id):
    destination=json.dumps([o._CONFIG,str(o._EXPERIMENT)])
    with connection() as c:
        c.execute('BEGIN IMMEDIATE')
        row=c.execute('SELECT payload FROM ticket_traces WHERE destination=? AND ticket_id=?',(destination,ticket_id)).fetchone()
        if row:
            state=json.loads(row[0])
        else:
            run=o._CLIENT.create_run(o._EXPERIMENT,tags={'mlflow.runName':ticket_id,'ticket_id':ticket_id,'trace_layout':'ticket'})
            state={'ticket_id':ticket_id,'trace_hex':uuid.uuid4().hex,'root_id':uuid.uuid4().hex[:16],
                   'run_id':run.info.run_id,'started_ns':time.time_ns(),'turn':0}
        state['turn']+=1
        c.execute('INSERT OR REPLACE INTO ticket_traces VALUES (?,?,?)',(destination,ticket_id,json.dumps(state)))
    state['trace_id']='tr-'+state['trace_hex']
    state['destination']=destination
    state['headers']={'traceparent':f"00-{state['trace_hex']}-{state['root_id']}-01"}
    return state


def publish_root(o, state, result=None, failed=False):
    from mlflow.entities import Span
    from mlflow.tracing.client import TracingClient
    summary=o.sanitize({k:result.get(k) for k in ('ticket_id','status','procedure_ref')}) if result else state.get('latest_result')
    if result:
        with connection() as c:
            row=c.execute('SELECT payload FROM ticket_traces WHERE destination=? AND ticket_id=?',(state['destination'],state['ticket_id'])).fetchone()
            saved=json.loads(row[0])
            if saved['turn']==state['turn']:
                saved['latest_result']=summary
                c.execute('UPDATE ticket_traces SET payload=? WHERE destination=? AND ticket_id=?',(json.dumps(saved),state['destination'],state['ticket_id']))
    attrs={'mlflow.traceRequestId':state['trace_id'],'mlflow.spanType':'AGENT',
           'session.id':state['ticket_id'],'folio.run_id':state['run_id'],
           'mlflow.spanInputs':{'ticket_id':state['ticket_id']},
           'folio.turns':state['turn'],'folio.last_operation_failed':failed}
    if summary:
        attrs['mlflow.spanOutputs']=summary
    # The root is a cumulative snapshot, not an in-memory span kept open during human waits.
    # Its ID stays fixed, so each upsert extends the same ticket trace after restarts.
    root=Span.from_dict_v2({'name':'ticket.'+state['ticket_id'],
        'context':{'trace_id':state['trace_hex'],'span_id':state['root_id']},'parent_id':None,
        'start_time':state['started_ns'],'end_time':time.time_ns(),
        'status_code':'OK','status_message':'','events':[],
        'attributes':{k:json.dumps(o.sanitize(v)) for k,v in attrs.items()}})
    TracingClient(o._CONFIG[0]).log_spans(str(o._EXPERIMENT),[root])
    o._CLIENT.link_traces_to_run([state['trace_id']],state['run_id'])
    o._CLIENT.set_tag(state['run_id'],'trace_id',state['trace_id'])
    o._CLIENT.set_trace_tag(state['trace_id'],'ticket_id',state['ticket_id'])
    o._CLIENT.set_trace_tag(state['trace_id'],'trace_layout','ticket')
    o._CLIENT.set_trace_tag(state['trace_id'],'last_operation_status','ERROR' if failed else 'OK')
    if result:
        o._CLIENT.set_trace_tag(state['trace_id'],'ticket_status',result['status'])
