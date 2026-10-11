import json
from datetime import datetime

import pytest
from test_api import client, providers, configure, add_doc, main

W=main.ticket_workflow


def sample(**changes):
    return dict(ticket_id='INC-00142',store_id='SW-0412',store_name='ServeWell - Koramangala',
        submitted_by='Maria Chen',contact_phone='+91-98765-43210',date_opened='2025-11-14T09:32:00+05:30',
        priority='P2',category='engineering',subcategory='Terminal Startup',subject='Terminal 2 will not start',
        description='Other terminals work.',asset_id='POS-0412-T2',system_version='FoodTech POS v4.2.1',
        tags=['engineering'],escalation_flag=False,related_tickets=[],ticket_history=[],resolution_notes=None,status='Open') | changes


def ticket(client,**changes):
    r=client.post('/api/tickets',json=sample(**changes));assert r.status_code==201,r.text
    return r.json()


def classification(**changes):
    return dict(intent='troubleshoot',immediate_triggers=[],do_not_escalate='none',reason='Single affected terminal.',base_priority='P3',overrides=[])|changes


def plan(**changes):
    return dict(action='clarify',message='What error message is displayed?',citations=[],query='',document_id='',offset=0)|changes


def setup_agent(client,providers,monkeypatch,cl=None):
    configure(client); doc=add_doc(client);main.ingest(doc)
    monkeypatch.setattr(W,'classify',lambda t,q:cl or classification())
    return doc


def ask(client,t,query='hybrid retrieval',request_id='request-001',**options):
    return client.post('/api/tickets/'+t['ticket_id']+'/query',json={'query':query,'version':t['version'],'request_id':request_id,'mode':'lexical',**options})


def outcome(client,t,**values):
    return client.post('/api/tickets/'+t['ticket_id']+'/confirm',json={'version':t['version'],'action_id':t['workflow']['pending']['id'],'outcome':'not_resolved','note':'Still not working','minutes_spent':15,**values})


def test_ticket_roundtrip_relations_history_auth(client):
    t=ticket(client,ticket_history=[{'timestamp':'2025-11-14T09:32:00+05:30','actor':'L1 Agent','note':'Customer reported incident.'}])
    assert t['ticket_history'][0]['note']=='Customer reported incident.'
    assert client.get('/api/tickets',headers={'Authorization':'Bearer wrong'}).status_code==401
    assert client.post('/api/tickets',json=sample()).status_code==409
    assert len(client.get('/api/tickets').json())==1
    for kind in ('stores','users','assets'):
        records=client.get('/api/ticket-directory/'+kind).json();assert len(records)==1
    with main.db() as c:
        row=c.execute('SELECT * FROM tickets').fetchone()
        assert row['submitted_by']==t['user_id'] and row['asset_id']=='POS-0412-T2'
        assert not c.execute('PRAGMA foreign_key_check').fetchall()
    assert client.put('/api/ticket-directory/labels',json={'label_id':'L1','ticket_id':t['ticket_id'],'correct_routing':'L2','should_escalate':True}).status_code==200
    assert client.put('/api/ticket-directory/labels',json={'label_id':'L2','ticket_id':'missing'}).status_code==422
    assert client.post('/api/tickets',json=sample(ticket_id='INC-2',store_id='OTHER')).status_code==409


def test_resolved_import_keeps_notes_and_blocks_agent(client):
    t=ticket(client,status='Resolved',resolution_notes='Updated driver. Customer verified print.')
    assert ask(client,t).status_code==409
    assert client.get('/api/tickets/'+t['ticket_id']).json()['resolution_notes']=='Updated driver. Customer verified print.'


def test_immediate_trigger_precedes_exclusion_and_checklist(client,providers,monkeypatch):
    setup_agent(client,providers,monkeypatch,classification(immediate_triggers=['payment_failure'],do_not_escalate='third_party',intent='escalate'))
    monkeypatch.setattr(W,'decision',lambda *a:pytest.fail('Immediate escalation must not troubleshoot'))
    providers.clear();t=ticket(client);r=ask(client,t);assert r.status_code==200,r.text
    t=r.json();assert t['status']=='Escalated' and t['priority']=='P1' and t['escalation_flag']
    assert t['workflow']['queue']=='L2 Support Team' and t['workflow']['missing_information']
    assert t['workflow']['notification_draft']['to']==['it-l2@servewell.in','oncall@servewell.in']
    assert t['workflow']['notification_draft']['sent'] is False
    assert not providers
    assert t['sla']['response_due']


def test_multihop_retrieval_cache_and_human_confirmation(client,providers,monkeypatch):
    doc=setup_agent(client,providers,monkeypatch)
    decisions=iter([plan(action='read',document_id=doc),plan(action='search',query='hybrid retrieval'),plan(action='step',message='Review the retrieval configuration.',citations=[doc+':0'])])
    monkeypatch.setattr(W,'decision',lambda *a:next(decisions))
    t=ticket(client);r=ask(client,t);assert r.status_code==200,r.text;t=r.json()
    assert t['status']=='Awaiting Customer'
    assert any(e.get('original') for e in t['workflow']['evidence'])
    assert any(x['action']=='retrieve' and x['metadata_filter']['tags_any']==['engineering'] for x in t['workflow']['trace'])
    assert not t['workflow'].get('steps')
    assert not any('User confirmed' in h['note'] for h in t['ticket_history'])
    # Same request is idempotent even with the old client version.
    repeated=ask(client,{**t,'version':1});assert repeated.status_code==200 and repeated.json()['version']==t['version']
    confirmed=outcome(client,t);assert confirmed.status_code==200,confirmed.text
    after=confirmed.json();assert after['workflow']['pending'] is None and after['workflow']['steps'][0]['minutes_spent']==15
    assert outcome(client,t).status_code==409
    monkeypatch.setattr(W,'retrieve',lambda *a:pytest.fail('Cached evidence should be reused'))
    monkeypatch.setattr(W,'decision',lambda *a:plan(action='resolve',message='Did that resolve the issue?',citations=[doc+':0']))
    r=ask(client,after,request_id='request-002');assert r.status_code==200,r.text
    t=r.json();assert t['status']!='Resolved'
    assert outcome(client,t,outcome='resolved',note='').status_code==422
    r=outcome(client,t,outcome='resolved',note='Customer verified normal operation.');assert r.status_code==200
    assert r.json()['status']=='Resolved' and r.json()['resolution_notes']=='Customer verified normal operation.'


def test_routine_escalation_requires_time_and_information(client,providers,monkeypatch):
    doc=setup_agent(client,providers,monkeypatch)
    monkeypatch.setattr(W,'decision',lambda *a:plan(action='escalate',message='Escalation needed.',citations=[doc+':0']))
    t=ask(client,ticket(client)).json()
    assert t['status']=='Awaiting Customer' and not t['escalation_flag']
    assert '15 minutes' in t['workflow']['pending']['message']
    t=outcome(client,t,outcome='answer',note='Will collect information.').json()
    monkeypatch.setattr(W,'decision',lambda *a:plan(action='step',message='Check the documented configuration.',citations=[doc+':0']))
    t=ask(client,t,request_id='request-002').json();t=outcome(client,t).json()
    info={k:'Confirmed' for k in W.REQUIRED};info.update(affected_devices=1,affected_users=2)
    r=client.put('/api/tickets/'+t['ticket_id']+'/information',json={'version':t['version'],'information':info});assert r.status_code==200,r.text;t=r.json()
    monkeypatch.setattr(W,'decision',lambda *a:plan(action='escalate',message='Still failing after checks.',citations=[doc+':0']))
    r=ask(client,t,request_id='request-003');assert r.status_code==200,r.text
    assert r.json()['status']=='Escalated' and not r.json()['workflow']['missing_information']


def test_do_not_escalate_and_unknown_citations(client,providers,monkeypatch):
    setup_agent(client,providers,monkeypatch,classification(do_not_escalate='billing'))
    monkeypatch.setattr(W,'decision',lambda *a:plan(action='escalate'))
    t=ask(client,ticket(client)).json();assert not t['escalation_flag'] and 'do-not-escalate' in t['workflow']['pending']['message']
    t=outcome(client,t,outcome='skipped').json()
    monkeypatch.setattr(W,'decision',lambda *a:plan(action='step',citations=['invented']))
    r=ask(client,t,request_id='request-002');assert r.status_code==502 and 'unknown citation' in r.json()['detail']


def test_new_urgent_information_supersedes_pending_action(client,providers,monkeypatch):
    setup_agent(client,providers,monkeypatch);monkeypatch.setattr(W,'decision',lambda *a:plan())
    t=ask(client,ticket(client)).json();assert t['workflow']['pending']
    monkeypatch.setattr(W,'classify',lambda *a:classification(immediate_triggers=['all_pos_down']))
    r=ask(client,t,query='Now all POS terminals are down.',request_id='request-002')
    assert r.status_code==200 and r.json()['status']=='Escalated'
    assert not r.json()['workflow']['pending']
    assert any('not marked completed' in h['note'] for h in r.json()['ticket_history'])


def test_agent_hop_limit_and_missing_source(client,providers,monkeypatch):
    setup_agent(client,providers,monkeypatch)
    calls=[]
    def decide(*args): calls.append(1);return plan(action='search',query='hybrid')
    monkeypatch.setattr(W,'decision',decide)
    r=ask(client,ticket(client));assert r.status_code==200
    assert len(calls)==4 and r.json()['workflow']['pending']['kind']=='clarify'
    t=outcome(client,r.json(),outcome='skipped').json()
    monkeypatch.setattr(W,'decision',lambda *a:plan(action='read',document_id='not-retrieved'))
    assert ask(client,t,request_id='request-002').status_code==502


def test_information_updates_asset_relation_and_validation(client):
    t=ticket(client)
    url='/api/tickets/'+t['ticket_id']+'/information'
    assert client.put(url,json={'version':t['version'],'information':{'affected_devices':-1}}).status_code==422
    assert client.put('/api/ticket-directory/assets',json={'asset_id':'NEW-ASSET','store_id':t['store_id'],'system_version':'Updated v2'}).status_code==200
    r=client.put(url,json={'version':t['version'],'information':{'asset_id':'NEW-ASSET','contact_phone':'12345'}});assert r.status_code==200
    with main.db() as c: assert c.execute('SELECT asset_id FROM tickets').fetchone()[0]=='NEW-ASSET'
    assert client.put(url,json={'version':t['version'],'information':{}}).status_code==409


def test_sla_table_business_hours_and_documented_pauses():
    t={'priority':'P2','workflow':{'escalated_at':'2026-10-11T12:00:00+05:30'}}
    s=W.sla_state(t)
    assert datetime.fromisoformat(s['response_due']).hour==13
    assert datetime.fromisoformat(s['halfway_check']).minute==30
    t={'priority':'P4','workflow':{'escalated_at':'2026-10-11T22:00:00+05:30'}}
    assert W.sla_state(t)['response_due']=='2026-10-12T14:00:00+05:30'
    t['workflow']['pauses']=[{'start':'2026-10-11T22:30:00+05:30','end':'2026-10-12T08:00:00+05:30'}]
    assert W.sla_state(t)['response_due']=='2026-10-12T15:30:00+05:30'


def test_priority_overrides_and_monitoring(client,providers,monkeypatch):
    t=sample(date_opened='2026-10-11T19:00:00+05:30')
    p,reason=W.priority(t,classification(base_priority='P3',overrides=['vip']))
    assert p=='P1' and 'peak_service_hours' in reason
    setup_agent(client,providers,monkeypatch,classification(immediate_triggers=['security']))
    t=ask(client,ticket(client)).json()
    for event in ['customer_wait','resume','l2_acknowledged','customer_updated']:
        r=client.post('/api/tickets/'+t['ticket_id']+'/monitor',json={'version':t['version'],'event':event,'note':'Confirmed by operator.'})
        assert r.status_code==200,r.text;t=r.json()
    assert t['sla']['acknowledged'] and not t['sla']['paused']


def test_escalated_ticket_can_be_resolved_only_after_confirmation(client,providers,monkeypatch):
    setup_agent(client,providers,monkeypatch,classification(immediate_triggers=['customer_escalation']))
    t=ask(client,ticket(client)).json()
    assert 'it-manager@servewell.in' in t['workflow']['notification_draft']['to']
    monkeypatch.setattr(W,'classify',lambda *a:classification(intent='resolve'))
    t=ask(client,t,query='L2 reports it fixed.',request_id='request-002').json()
    assert t['status']=='Escalated' and t['workflow']['pending']['kind']=='resolve'
    r=outcome(client,t,outcome='resolved',note='Customer verified a successful transaction.')
    assert r.status_code==200 and r.json()['status']=='Resolved'
    assert not r.json()['sla']['breached']


def test_metadata_filter_is_applied_to_retrieval(client,providers):
    configure(client);doc=add_doc(client);main.ingest(doc)
    r=client.post('/api/search',json={'query':'hybrid','mode':'lexical','rerank':False,'tags':['not-present']})
    assert r.json()['results']==[]
    providers.clear()
    client.post('/api/search',json={'query':'hybrid','mode':'vector','rerank':False,'tags':['engineering']})
    args=next(b for u,b in providers if u.endswith('/query'))
    assert {'tags':{'$in':['engineering']}} in args['filter']['$and']
    assert {'document_id':{'$in':[doc]}} in args['filter']['$and']

