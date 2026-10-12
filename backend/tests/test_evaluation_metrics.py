from evaluation import dataset, metrics


def test_retrieval_metrics_match_on_filename_and_skip_the_procedure():
    label={'relevant_kb_docs':['runbooks/printer-offline.md','faq/printers-faq.md','sop/escalation-procedure.md']}
    relevant=metrics.relevant_documents(label)
    assert relevant=={'printer-offline.md','printers-faq.md'}
    r=metrics.retrieval(relevant,['pos-faq.md','printer-offline.md','printer-offline.md','star-printer.md'],k=3)
    assert r=={'recall':0.5,'hit':1.0,'precision':1/3,'rr':0.5}
    assert metrics.retrieval(set(),['x.md']) is None
    assert metrics.retrieval({'a.md'},[])['rr']==0.0


def test_binary_reports_both_escalation_error_types():
    m=metrics.binary([(True,True),(True,False),(False,True),(False,False),(False,False)])
    assert (m['tp'],m['fn'],m['fp'],m['tn'])==(1,1,1,2)
    assert m['missed_escalation_rate']==0.5 and m['unnecessary_escalation_rate']==1/3
    assert metrics.binary([(True,True)])['specificity'] is None


def test_workflow_route_mapping():
    assert metrics.workflow_route({'status':'Escalated','workflow':{}})=='l2_escalation'
    assert metrics.workflow_route({'status':'Awaiting Customer','workflow':{'pending':{'kind':'step'}}})=='l1_guided'
    assert metrics.workflow_route({'status':'Awaiting Customer','workflow':{'pending':{'kind':'clarify'}}})=='needs_clarification'
    assert metrics.workflow_route({'status':'In Progress','workflow':{'pending':None}})=='no_supported_step'


def test_split_is_stratified_disjoint_and_deterministic():
    cases={}
    for i in range(40):
        cases[f'T{i}']={'ticket':{'category':'POS' if i%2 else 'Kiosks'},'label':{'correct_routing':'l1_guided' if i%4<2 else 'l2_escalation'}}
    cases['C1']={'ticket':{'category':'POS'},'label':None}
    a=dataset.make_split(cases);b=dataset.make_split(cases)
    assert a==b and not set(a['dev'])&set(a['holdout'])
    assert len(a['holdout'])==12 and a['adversarial']==['C1']
