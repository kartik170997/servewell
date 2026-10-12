import copy
from test_api import client, providers, main
from test_live_workflow import live, start, final, feedback

L=main.live_workflow


def test_citation_and_confidence_persist_on_message_and_pending(client,live,monkeypatch):
    original=L.plan
    def planned(t,q):
        result=copy.deepcopy(original(t,q))
        support={'citations':[live+':0'],'confidence':0.72,'confidence_reason':'Supported by the retrieved document; outcome unknown.'}
        result.update(support)
        for step in result['steps']: step.update(support)
        return result
    monkeypatch.setattr(L,'plan',planned)
    t=final(start(client))
    assert t['workflow']['pending']['confidence']==0.72
    assert t['workflow']['pending']['citations']==[live+':0']
    assert t['workflow']['messages'][-1]['confidence']==0.72
    loaded=client.get('/api/live/'+t['ticket_id']).json()
    assert loaded['workflow']['plan_support']['confidence']==0.72


def test_model_cannot_attach_invented_citations(client,live,monkeypatch):
    import dspy
    import pytest
    from dspy.utils import DummyLM
    from test_tickets import classification
    monkeypatch.setattr(dspy,'LM',lambda *a,**kw:DummyLM([
        {'classification':classification(citations=['invented-source'])}],adapter=dspy.JSONAdapter()))
    with pytest.raises(ValueError,match='output-format error'):
        L.predict(L.classify_signature(),'classification',{'query':'A terminal is frozen.'})


def test_missing_confidence_is_not_fabricated(client,live,monkeypatch):
    import dspy
    import pytest
    from dspy.utils import DummyLM
    from test_tickets import classification
    monkeypatch.setattr(dspy,'LM',lambda *a,**kw:DummyLM([
        {'classification':classification(confidence=None)}],adapter=dspy.JSONAdapter()))
    with pytest.raises(ValueError,match='output-format error'):
        L.predict(L.classify_signature(),'classification',{'query':'A terminal is frozen.'})


def test_native_schema_is_sent_and_retries_are_bounded(client,live,monkeypatch):
    import dspy
    import pytest
    from dspy.utils import DummyLM
    from test_tickets import classification
    calls=[]
    class InspectLM(DummyLM):
        def __call__(self,*args,**kwargs):
            calls.append(kwargs)
            return super().__call__(*args,**kwargs)
    lm=InspectLM([{'classification':classification(confidence=2)}],adapter=dspy.JSONAdapter())
    monkeypatch.setattr(dspy,'LM',lambda *a,**kw:lm)
    monkeypatch.setenv('WORKFLOW_OUTPUT_MAX_RETRIES','2')
    with pytest.raises(ValueError,match='after 3 attempts'):
        L.predict(L.classify_signature(),'classification',{'query':'A terminal is frozen.'})
    assert len(calls)==3
    schema=calls[0]['output_config']['format']['schema']
    assert calls[0]['output_config']['format']['type']=='json_schema'
    assert schema['additionalProperties'] is False
    assert schema['required']==['classification']
    model=schema['$defs']['LiveClassification']
    assert {'confidence','confidence_reason','citations'}.issubset(model['required'])
    assert 'maximum' not in model['properties']['confidence']
    # Provider gets supported grammar; local validation still rejects confidence=2.


def test_questions_are_not_suppressed_or_rewritten(client,live,monkeypatch):
    original=L.plan
    question='What is the store name and contact phone?'
    def planned(t,q):
        result=original(t,q)
        result.update(evidence_action='clarify',question=question)
        return result
    monkeypatch.setattr(L,'plan',planned)
    t=final(start(client))
    assert t['workflow']['pending']['message']==question
    t=final(feedback(client,t,outcome='answer',note="The phone is available at the store"))
    assert t['workflow']['pending']['kind']=='clarify'
    assert t['workflow']['pending']['message']==question
    assert not t['workflow'].get('questions')


def test_two_planning_questions_then_step_across_checkpoint_resumes(client,live,monkeypatch):
    original=L.plan
    def planned(t,q):
        result=original(t,q)
        result.update(evidence_action='clarify',question='What is the symptom? What is the version?')
        return result
    monkeypatch.setattr(L,'plan',planned)
    t=final(start(client))
    assert t['workflow']['pending']['message']=='What is the symptom?'
    assert t['workflow']['planning_questions_asked']==1
    t=final(feedback(client,t,outcome='answer',note="The screen is frozen"))
    assert t['workflow']['pending']['kind']=='clarify'
    assert t['workflow']['planning_questions_asked']==2
    t=final(feedback(client,t,outcome='answer',note="Still don't know"))
    assert t['workflow']['pending']['kind']=='step'
    assert t['workflow']['planning_questions_asked']==2
    assert t['workflow']['plan'][0]['status']=='active'
    assert not t['workflow']['plan'][0]['feedback']


def test_one_question_config_and_no_evidence_does_not_loop(client,live,monkeypatch):
    monkeypatch.setenv('WORKFLOW_PLANNING_MAX_QUESTIONS','1')
    monkeypatch.setattr(L,'plan',lambda *a:{'summary':'No supported steps','steps':[],
        'evidence_action':'clarify','question':'What is the symptom?'})
    t=final(start(client))
    t=final(feedback(client,t,outcome='answer',note='Unknown'))
    # With the question budget spent, the agent falls back to the pinned procedure's
    # standard L1 steps instead of asking again or inventing device-specific instructions.
    assert t['workflow']['planning_questions_asked']==1
    assert t['workflow']['pending']['kind']=='step'
    assert t['workflow']['pending']['citations']==[L.procedure_citation(t)]
    assert not t['workflow'].get('planning_blocked_reason')
    assert not t['escalation_flag']


def test_no_evidence_and_no_procedure_steps_stops_for_l1_review(client,live,monkeypatch):
    monkeypatch.setenv('WORKFLOW_PLANNING_MAX_QUESTIONS','1')
    original_fallback=L.standard_procedure_steps
    monkeypatch.setattr(L,'standard_procedure_steps',lambda t:[])
    monkeypatch.setattr(L,'plan',lambda *a:{'summary':'No supported steps','steps':[],
        'evidence_action':'clarify','question':'What is the symptom?'})
    t=final(start(client))
    t=final(feedback(client,t,outcome='answer',note='Unknown'))
    assert t['workflow']['pending'] is None
    assert not t['workflow']['checkpoint']['paused']
    assert t['workflow']['planning_blocked_reason']
    assert not t['escalation_flag']
    monkeypatch.setattr(L,'standard_procedure_steps',original_fallback)
    t=final(client.post('/api/live/'+t['ticket_id']+'/resume',json={'version':t['version']}))
    assert t['workflow']['pending']['kind']=='step'
    assert not t['workflow'].get('planning_blocked_reason')


def test_existing_answers_count_toward_planning_cap(client,live):
    t={'workflow':{'steps':[{'outcome':'answer'},{'outcome':'answer'}]}}
    assert L.planning_questions_remaining(t)==0


def test_unknown_answer_uses_sop_immediately(client,live,monkeypatch):
    monkeypatch.setattr(L,'plan',lambda *a:{'summary':'No document step','steps':[],
        'evidence_action':'clarify','question':'What is the error code?'})
    t=final(start(client))
    t=final(feedback(client,t,outcome='answer',note="I don't know, screen is frozen"))
    assert t['workflow']['pending']['kind']=='step'
    assert t['workflow']['planning_questions_asked']==1
    assert t['workflow']['pending']['citations']==[L.procedure_citation(t)]


def test_sop_fallback_preserves_old_plan_and_original_report(client,live):
    t=final(start(client))
    t['description']='I already tried a soft reboot but the terminal is still frozen.'
    t['workflow']['plan'][0]['status']='completed'
    t['workflow']['plan'][1]['status']='failed'
    t['workflow']['steps']=[{'kind':'clarify','outcome':'answer','note':'I do not know','step':'Error code?'}]
    assert L.proceed_after_planning(t)=='prepare'
    assert t['workflow']['plan'][0]['status']=='completed'
    assert t['workflow']['plan'][1]['status']=='failed'
    fallback=[s for s in t['workflow']['plan'] if s.get('procedure_instruction')]
    assert fallback
    assert not any('restart' in s['instructions'].lower() for s in fallback)
