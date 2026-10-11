import json
import pytest
from test_api import client,providers,configure,add_doc,main
from test_tickets import classification, sample

L=main.live_workflow
W=main.ticket_workflow


def events(response):
    assert response.status_code==200,response.text
    return [json.loads(line) for line in response.text.splitlines() if line.strip()]


def final(response):
    stream=events(response)
    assert not any(e['type']=='error' for e in stream),stream[-1]
    return next(e['ticket'] for e in reversed(stream) if e['type']=='result')


@pytest.fixture
def live(client,providers,monkeypatch):
    configure(client);doc=add_doc(client);main.ingest(doc)
    monkeypatch.setattr(L,'classify',lambda *a:classification())
    monkeypatch.setattr(L,'assess',lambda *a:{'next_action':'continue','reason':'Proceed with the existing checklist.'})
    def planned(*a):
        return {'summary':'Two supported checks.','evidence_action':'sufficient','steps':[
            {'title':'Inspect configuration','instructions':'Compare the retrieval configuration with the guide.','expected_result':'Configuration matches.','citations':[doc+':0']},
            {'title':'Check retrieval','instructions':'Run the documented retrieval verification.','expected_result':'Expected results appear.','citations':[doc+':0']}]}
    monkeypatch.setattr(L,'plan',planned)
    return doc


def start(client,**changes):
    return client.post('/api/live/start',json={'query':'hybrid retrieval is not working','request_id':'live-start-001','mode':'lexical',**changes})


def feedback(client,t,**changes):
    return client.post('/api/live/'+t['ticket_id']+'/feedback',json={'version':t['version'],'action_id':t['workflow']['pending']['id'],
        'outcome':'not_resolved','note':'Completed the check, still not working.','minutes_spent':8,**changes})


def test_real_graph_interrupt_resume_and_restart(client,live,monkeypatch):
    response=start(client);stream=events(response);t=final(response)
    assert {'classify','retrieve','plan','prepare'}.issubset({e.get('node') for e in stream if e['type']=='stage'})
    assert t['workflow']['engine']=='LangGraph + DSPy'
    assert t['workflow']['checkpoint']['paused']
    assert [x['status'] for x in t['workflow']['plan']]==['active','pending']
    assert not t['workflow'].get('steps')
    assert (main.DATA/'workflow-checkpoints.sqlite').exists()
    before=t['workflow']['checkpoint']['id']
    # A fresh graph and SQLite connection are built for every request, as after a restart.
    monkeypatch.setattr(L,'plan',lambda *a:pytest.fail('Resuming must not regenerate a checklist.'))
    t=final(feedback(client,t))
    assert t['workflow']['checkpoint']['id']!=before
    assert [x['status'] for x in t['workflow']['plan']]==['failed','active']
    assert len(t['workflow']['steps'])==1
    t=final(feedback(client,t,outcome='resolved',note='User verified the issue is fixed.'))
    assert t['status']=='Resolved' and t['resolution_notes']=='User verified the issue is fixed.'
    assert not t['workflow']['checkpoint']['paused']
    assert len([h for h in t['ticket_history'] if h['note'].startswith('Feedback:')])==2


def test_exhausted_checklist_automatically_checks_then_escalates(client,live):
    t=final(start(client,submitted_by='Operator',contact_phone='123',asset_id='ASSET-1'))
    t=final(feedback(client,t));t=final(feedback(client,t))
    assert t['workflow']['pending']['kind']=='information' and not t['escalation_flag']
    info={k:'Reported value' for k in W.REQUIRED};info.update(affected_devices=1,affected_users=1)
    t=client.put('/api/tickets/'+t['ticket_id']+'/information',json={'version':t['version'],'information':info}).json()
    t=final(feedback(client,t,outcome='answer',note='Required information is now complete.'))
    assert t['status']=='Escalated' and t['workflow']['queue']=='L2 Support Team'
    assert t['workflow']['notification_draft']['sent'] is False
    assert not t['workflow']['pending']


def test_durable_failure_can_resume_without_reclassifying(client,live,monkeypatch):
    original=L.plan
    monkeypatch.setattr(L,'plan',lambda *a:(_ for _ in ()).throw(ValueError('Temporary planning failure')))
    stream=events(start(client));assert stream[-1]['type']=='error'
    ticket_id=stream[0]['ticket']['ticket_id'];t=client.get('/api/tickets/'+ticket_id).json()
    assert t['workflow']['checkpoint']['recoverable']
    assert t['workflow']['checkpoint']['next']==['plan']
    monkeypatch.setattr(L,'plan',original)
    monkeypatch.setattr(L,'classify',lambda *a:pytest.fail('Successful classification is already checkpointed.'))
    t=final(client.post('/api/live/'+ticket_id+'/resume',json={'version':t['version']}))
    assert t['workflow']['checkpoint']['paused'] and len(t['workflow']['plan'])==2


def test_duplicate_feedback_and_blank_feedback_are_rejected(client,live):
    t=final(start(client));original=t
    response=feedback(client,t,note='');assert events(response)[-1]['status']==422
    t=final(feedback(client,t))
    assert events(feedback(client,original))[-1]['status']==409
    again=final(start(client))
    assert again['ticket_id']==t['ticket_id']
    assert len(again['workflow']['steps'])==1


def test_immediate_escalation_bypasses_planning(client,live,monkeypatch):
    monkeypatch.setattr(L,'classify',lambda *a:classification(immediate_triggers=['payment_failure']))
    monkeypatch.setattr(L,'plan',lambda *a:pytest.fail('Do not troubleshoot an immediate escalation.'))
    t=final(start(client));assert t['status']=='Escalated' and t['priority']=='P1'


def test_planner_can_retrieve_again_then_read_original(client,live,monkeypatch):
    original=L.plan;calls=[]
    def planned(*a):
        calls.append(1)
        if len(calls)==1:return {'summary':'Need specific source','evidence_action':'search','retrieval_query':'hybrid'}
        if len(calls)==2:return {'summary':'Need original details','evidence_action':'read','document_id':live,'offset':0}
        return original(*a)
    monkeypatch.setattr(L,'plan',planned)
    t=final(start(client))
    assert len(calls)==3
    assert any(e.get('original') for e in t['workflow']['evidence'])
    assert t['workflow']['pending']['kind']=='step'


def test_four_hop_limit_and_bad_citations(client,live,monkeypatch):
    calls=[]
    def more(*a): calls.append(1);return {'summary':'Need more','evidence_action':'search','retrieval_query':'hybrid'}
    monkeypatch.setattr(L,'plan',more)
    t=final(start(client));assert len(calls)==4 and t['workflow']['pending']['kind']=='clarify'
    monkeypatch.setattr(L,'plan',lambda *a:{'summary':'Wrong','evidence_action':'sufficient','steps':[{'title':'X','instructions':'X','expected_result':'X','citations':['invented']}]})
    assert events(feedback(client,t,outcome='answer',note='Here is the error.'))[-1]['type']=='error'


def test_new_feedback_can_trigger_immediate_escalation(client,live,monkeypatch):
    t=final(start(client))
    monkeypatch.setattr(L,'classify',lambda *a:classification(immediate_triggers=['security']))
    t=final(feedback(client,t,note='New evidence indicates a security incident.'))
    assert t['status']=='Escalated'


def test_feedback_can_retrieve_and_replan_without_repeating_failed_steps(client,live,monkeypatch):
    t=final(start(client))
    monkeypatch.setattr(L,'assess',lambda *a:{'next_action':'retrieve','reason':'New symptom','retrieval_query':'hybrid retrieval'})
    t=final(feedback(client,t,note='The check failed and a new symptom appeared.'))
    assert t['workflow']['plan'][0]['status']=='failed'
    assert len(t['workflow']['plan'])==2
    assert t['workflow']['plan'][1]['status']=='active'
    assert any(x.get('action')=='evaluate' and x.get('next_action')=='retrieve' for x in t['workflow']['trace'])


def test_dspy_signatures_and_adapter_are_really_used(client,live,monkeypatch):
    import dspy
    from dspy.utils import DummyLM
    def model(*args, **kwargs):
        assert 'temperature' not in kwargs
        return DummyLM([{'classification':classification()}])
    monkeypatch.setattr(dspy,'LM',model)
    # This exercises Predict + typed ChatAdapter against the actual signature, without a provider call.
    result=L.predict(L.classify_signature(),'classification',{'query':'A single terminal is down.'})
    assert result['base_priority']=='P3'


def test_planner_maps_only_valid_source_aliases(client,providers,monkeypatch):
    configure(client)
    t={'ticket_history':[],'workflow':{'classification':{},'steps':[],'messages':[],
        'evidence':[{'id':'long-document-id:0@16000','document_id':'long-document-id','text':'Source text'}]}}
    def predicted(*args):
        context=args[-1]
        assert context['allowed_citation_ids']==['S1']
        assert context['evidence'][0]['id']=='S1'
        return {'steps':[{'title':'Check','instructions':'Check source','expected_result':'Pass','citations':['S1']}],'document_id':'S1'}
    monkeypatch.setattr(L,'predict',predicted)
    result=L.plan(t,'Query')
    assert result['steps'][0]['citations']==['long-document-id:0@16000']
    assert result['document_id']=='long-document-id'
    monkeypatch.setattr(L,'predict',lambda *a:{'steps':[{'citations':['S99']}]})
    with pytest.raises(ValueError,match='outside the retrieved evidence'):L.plan(t,'Query')


def test_restore_reconciles_graph_checkpoint_after_projection_loss(client,live):
    t=final(start(client));checkpoint=t['workflow']['checkpoint']['id']
    # Simulate a restart between the graph's durable write and UI projection.
    with main.db() as c:
        c.execute('UPDATE ticket_workflow SET payload=? WHERE ticket_id=?',(json.dumps({'evidence':[],'messages':[],'trace':[],'pending':None}),t['ticket_id']))
    restored=client.get('/api/live/'+t['ticket_id']).json()
    assert restored['workflow']['checkpoint']['id']==checkpoint
    assert restored['workflow']['pending']['kind']=='step'
