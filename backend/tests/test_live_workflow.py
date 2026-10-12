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
    client.put('/api/ticket-directory/stores',json={'store_id':'TEST-STORE','store_name':'Test store','city':'Mumbai'})
    client.put('/api/ticket-directory/assets',json={'asset_id':'ASSET-1','store_id':'TEST-STORE','asset_type':'POS Terminal','system_version':'POS v1'})
    original_predict=L.predict
    def predicted(signature,*args):
        if signature is L.InformationSignature: return {'ticket_updates':[],'checklist_updates':[]}
        return original_predict(signature,*args)
    monkeypatch.setattr(L,'predict',predicted)
    monkeypatch.setattr(L,'classify',lambda *a:classification())
    monkeypatch.setattr(L,'assess',lambda *a:{'next_action':'continue','reason':'Proceed with the existing checklist.'})
    def planned(*a):
        return {'summary':'Two supported checks.','evidence_action':'sufficient','steps':[
            {'title':'Inspect configuration','instructions':'Compare the retrieval configuration with the guide.','expected_result':'Configuration matches.','citations':[doc+':0']},
            {'title':'Check retrieval','instructions':'Run the documented retrieval verification.','expected_result':'Expected results appear.','citations':[doc+':0']}]}
    monkeypatch.setattr(L,'plan',planned)
    return doc


def start(client,**changes):
    return client.post('/api/live/start',json={'query':'hybrid retrieval is not working','request_id':'live-start-001','mode':'lexical','asset_id':'ASSET-1',**changes})


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
        return DummyLM([{'classification':classification()}],adapter=dspy.JSONAdapter())
    monkeypatch.setattr(dspy,'LM',model)
    # This exercises Predict + typed ChatAdapter against the actual signature, without a provider call.
    result=L.predict(L.classify_signature(),'classification',{'query':'A single terminal is down.'})
    assert result['base_priority']=='P3'


def test_python_constructor_output_reports_format_error(client,live,monkeypatch):
    import dspy
    import pytest
    from dspy.utils import DummyLM
    monkeypatch.setattr(dspy,'LM',lambda *a,**kw:DummyLM([
        {'classification':'LiveClassification(intent="troubleshoot", base_priority="P3")'}],adapter=dspy.JSONAdapter()))
    with pytest.raises(ValueError,match='output-format error, not an API-key error'):
        L.predict(L.classify_signature(),'classification',{'query':'A terminal is down.'})


def test_invalid_output_is_retried_and_reminder_requires_json(client,live,monkeypatch):
    import dspy
    from dspy.utils import DummyLM
    lm=DummyLM([{'classification':'LiveClassification(intent="troubleshoot")'},
                {'classification':classification()}],adapter=dspy.JSONAdapter())
    monkeypatch.setattr(dspy,'LM',lambda *a,**kw:lm)
    signature=L.classify_signature()
    reminder=L.ProcedureChatAdapter({}).user_message_output_requirements(signature)
    assert 'valid Python' not in reminder
    assert 'enforced schema' in reminder
    assert 'classification' in reminder
    assert '[[ ##' not in reminder
    result=L.predict(signature,'classification',{'query':'A terminal is down.'})
    assert result['base_priority']=='P3'


def test_planner_maps_only_valid_source_aliases(client,providers,monkeypatch):
    configure(client)
    t={'ticket_history':[],'workflow':{'classification':{},'steps':[],'messages':[],
        'evidence':[{'id':'long-document-id:0@16000','document_id':'long-document-id','text':'Source text'}]}}
    t['workflow'].update(original_issue='Original frozen terminal',plan=[{'title':'Earlier check','status':'completed'}],
        steps=[{'step':str(i)} for i in range(45)],messages=[{'text':str(i)} for i in range(50)])
    def predicted(*args):
        context=args[-1]
        # Evidence aliases plus the pinned procedure, which is citable for standard L1 steps.
        assert context['allowed_citation_ids']==['S1',L.procedure_citation(t)]
        assert context['evidence'][0]['id']=='S1'
        assert len(context['confirmed_steps'])==45
        assert len(context['recent_messages'])==50
        assert context['original_issue']=='Original frozen terminal'
        assert context['earlier_plan'][0]['status']=='completed'
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


def test_start_resolves_asset_relationships_and_ignores_spoofed_context(client,live,monkeypatch):
    seen=[]
    def classified(t,q):
        seen.append(t)
        return classification()
    monkeypatch.setattr(L,'classify',classified)
    assert start(client,store_id='SPOOF').status_code==422
    t=final(start(client,store_id='TEST-STORE',system_version='SPOOF'))
    assert t['store_id']=='TEST-STORE' and t['store_name']=='Test store'
    assert t['system_version']=='POS v1'
    assert t['store_details']['city']=='Mumbai'
    assert seen[0]['asset_details']['asset_type']=='POS Terminal'
    assert t['escalation_info']['asset_type']=='POS Terminal'
    assert client.get('/api/asset-context/ASSET-1').json()['store']['store_id']=='TEST-STORE'


def test_unknown_asset_does_not_create_workflow(client,live):
    assert start(client,asset_id='UNKNOWN').status_code==404
    assert start(client,asset_id=' ').status_code==422
    assert client.get('/api/tickets').json()==[]


def test_store_only_workflow_populates_checklist(client,live):
    # Asset is not guessed when a store has several devices.
    t=final(start(client,asset_id='',store_id='TEST-STORE'))
    assert t['asset_id']==''
    assert t['escalation_info']['store_id']=='TEST-STORE'
    assert t['escalation_info']['store_name']=='Test store'
    assert t['escalation_info']['city']=='Mumbai'


def test_feedback_tools_persist_facts_through_projection_and_restart(client,live,monkeypatch):
    t=final(start(client))
    original=L.predict
    def predicted(signature,*args):
        if signature is L.InformationSignature:
            return {'checklist_updates':[{'field':'contact_phone','value':'12345','evidence':'phone 12345'}],
                'ticket_updates':[{'field':'subcategory','value':'Printer','evidence':'Printer'}]}
        return original(signature,*args)
    monkeypatch.setattr(L,'predict',predicted)
    t=final(feedback(client,t,note='Printer still fails. My phone 12345.'))
    restored=client.get('/api/live/'+t['ticket_id']).json()
    assert restored['contact_phone']=='12345' and restored['escalation_info']['contact_phone']=='12345'
    assert restored['subcategory']=='Printer'
    assert len([h for h in restored['ticket_history'] if h['actor']=='Agent tool'])==2
    restored=client.get('/api/live/'+t['ticket_id']).json()
    assert len([h for h in restored['ticket_history'] if h['actor']=='Agent tool'])==2


def test_unquoted_model_facts_are_not_saved(client,live,monkeypatch):
    monkeypatch.setattr(L,'classify',lambda *a:{**classification(),'checklist_updates':[{'field':'contact_phone','value':'invented','evidence':'not in user query'}]})
    t=final(start(client))
    assert not t['contact_phone']


def test_store_id_in_first_feedback_is_saved_to_checklist(client,live):
    client.put('/api/ticket-directory/stores',json={'store_id':'SW-1234','store_name':'Store from feedback','city':'Pune'})
    t=final(start(client,asset_id='',store_id='TEST-STORE'))
    t=final(feedback(client,t,note='The store ID is SW-1234. The step did not fix it.'))
    assert t['store_id']=='SW-1234'
    assert t['escalation_info']['store_id']=='SW-1234'
    assert t['escalation_info']['store_name']=='Store from feedback'
    assert client.get('/api/live/'+t['ticket_id']).json()['store_id']=='SW-1234'


def test_external_ticket_tool_changes_survive_graph_resume(client,live):
    t=final(start(client))
    r=client.post('/api/agent/tools/update_ticket',json={'ticket_id':t['ticket_id'],'version':t['version'],'arguments':{'fields':{'subject':'Confirmed issue description'}}})
    assert r.status_code==200
    t=client.get('/api/live/'+t['ticket_id']).json()
    assert t['subject']=='Confirmed issue description'
    t=final(feedback(client,t))
    assert t['subject']=='Confirmed issue description'


def test_priority_criterion_must_come_from_the_active_procedure():
    procedure='- **High (P2)**: Single location partial outage, 50%+ of POS terminals down\n- **Medium (P3)**: Single terminal down'
    grounded=classification(base_priority='P2',priority_criterion='High (P2): Single location partial outage, 50%+ of POS terminals down')
    assert L.consistency_reason('classification',grounded,procedure) is None
    assert L.consistency_reason('classification',classification(priority_criterion='Most machines down means P2'),procedure)=='priority_criterion_not_in_procedure'
    assert L.consistency_reason('classification',classification(priority_criterion=''),procedure)=='priority_criterion_not_in_procedure'
    mismatch=classification(base_priority='P3',priority_criterion='High (P2): Single location partial outage')
    assert L.consistency_reason('classification',mismatch,procedure)=='priority_criterion_mismatch'


def test_priority_reason_cites_the_procedure_criterion():
    t={'date_opened':'2026-10-12T09:00:00+05:30'}
    p,reason=W.priority(t,classification(base_priority='P2',priority_criterion='High (P2): 50%+ of POS terminals down'))
    assert p=='P2' and 'procedure: "High (P2): 50%+ of POS terminals down"' in reason
