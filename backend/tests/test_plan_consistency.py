from test_api import client, providers, main
from test_live_workflow import live

L=main.live_workflow


def support(cite):
    return {'citations':[cite],'confidence':0.6,'confidence_reason':'Procedure supports standard checks.'}


def procedure_cite():
    p=L.W.procedure_for(None)
    return 'procedure:'+str(p.get('id','SOP-IT-L1-002'))+':v'+str(p.get('version',1))


def test_consistency_reason_rules():
    assert L.consistency_reason('plan',{'evidence_action':'sufficient','steps':[]})=='plan_without_steps'
    assert L.consistency_reason('plan',{'evidence_action':'clarify','question':'steps'})=='clarify_without_question'
    assert L.consistency_reason('assessment',{'next_action':'clarify','question':''})=='clarify_without_question'
    assert L.consistency_reason('plan',{'evidence_action':'clarify','question':'Which terminal is affected?'}) is None
    assert L.consistency_reason('plan',{'evidence_action':'sufficient','steps':[{'title':'x'}]}) is None
    assert L.consistency_reason('plan',{'evidence_action':'search','steps':[]}) is None


def test_sufficient_plan_without_steps_is_regenerated(client,live,monkeypatch):
    # Observed in evaluation: steps written into summary, steps=[] and question="steps".
    import dspy
    from dspy.utils import DummyLM
    cite=procedure_cite()
    empty={'plan':{**support(cite),'summary':'Run the basic checks below.','steps':[],'evidence_action':'sufficient','question':'steps'}}
    good={'plan':{**support(cite),'summary':'Basic checks.','evidence_action':'sufficient','steps':[
        {**support(cite),'title':'Restart terminal','instructions':'Restart the terminal.','expected_result':'Terminal starts.'}]}}
    calls=[]
    class InspectLM(DummyLM):
        def __call__(self,*args,**kwargs):
            calls.append(kwargs.get('messages') or args)
            return super().__call__(*args,**kwargs)
    lm=InspectLM([empty,good],adapter=dspy.JSONAdapter())
    monkeypatch.setattr(dspy,'LM',lambda *a,**kw:lm)
    monkeypatch.setenv('WORKFLOW_OUTPUT_MAX_RETRIES','2')
    result=L.predict(L.PlanningSignature,'plan',{'query':'Terminal frozen.','allowed_citation_ids':[cite]})
    assert len(calls)==2
    assert [s['title'] for s in result['steps']]==['Restart terminal']
    assert 'steps was empty' in str(calls[1])


def test_plan_schema_requires_steps():
    adapter=L.ProcedureChatAdapter({'text':'x'},['S1'],['S1'])
    assert 'steps' in adapter.output_schema(L.PlanningSignature)['$defs']['PlanResult']['required']
