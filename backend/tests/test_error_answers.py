import pytest
from test_api import client, providers, configure, add_doc, main
from test_live_workflow import live, start, final, feedback, L, W


def test_error_answer_reads_original_and_survives_checkpoint(client,live,monkeypatch):
    doc=add_doc(client,b'Printer error E42 means the cover is open. Close the cover and print a test receipt.',name='printer-errors.md')
    main.ingest(doc)
    def planned(t,query):
        sources=[e for e in t['workflow']['evidence'] if e.get('original') and 'E42' in e['text']]
        assert sources
        return {'summary':'Error E42','answer':'E42 indicates an open printer cover. Close it and try printing.',
                'answer_citations':[sources[0]['id']],'steps':[],'evidence_action':'sufficient'}
    monkeypatch.setattr(L,'plan',planned)
    t=final(start(client,query='hybrid printer error E42: what does it mean?'))
    assert t['escalation_info']['error_code']=='E42'
    assert t['workflow']['direct_answer']['text'].startswith('E42')
    assert t['workflow']['pending']['kind']=='clarify'
    assert t['workflow']['plan']==[]
    assert client.get('/api/live/'+t['ticket_id']).json()['workflow']['direct_answer']==t['workflow']['direct_answer']


def test_new_query_fetches_new_evidence_even_with_existing_sources(client,live,monkeypatch):
    t=final(start(client))
    calls=[];original=W.retrieve
    def retrieve(*args,**kwargs):
        calls.append(args[1]);return original(*args,**kwargs)
    monkeypatch.setattr(W,'retrieve',retrieve)
    response=client.post('/api/live/'+t['ticket_id']+'/query',json={'query':'hybrid error E42','version':t['version'],'request_id':'new-error-question','mode':'lexical'})
    t=final(response)
    assert calls and 'E42' in calls[0]
    assert t['escalation_info']['error_code']=='E42'


def test_unknown_error_does_not_return_generic_procedure_as_answer(client,monkeypatch):
    t={'ticket_history':[],'escalation_info':{'error_code':'E99'},'workflow':{'classification':{},'steps':[],
       'messages':[],'evidence':[{'id':'doc:0','text':'L1 escalation requires recording all checklist fields.'}]}}
    monkeypatch.setattr(L,'predict',lambda *a:{'summary':'Procedure','answer':'Collect the full checklist.',
        'answer_citations':['S1'],'steps':[],'evidence_action':'sufficient'})
    result=L.plan(t,'What does error E99 mean?')
    assert result['evidence_action']=='clarify'
    assert result['answer']=='' and result['steps']==[]
    assert 'could not verify' in result['question']


def test_error_in_feedback_reclassifies_before_remaining_checklist(client,live,monkeypatch):
    t=final(start(client))
    calls=[];original=W.retrieve
    def retrieve(*args,**kwargs): calls.append(args[1]);return original(*args,**kwargs)
    monkeypatch.setattr(W,'retrieve',retrieve)
    t=final(feedback(client,t,note='The display now shows error E42. hybrid printer still fails.'))
    assert calls and 'E42' in calls[0]
    assert t['escalation_info']['error_code']=='E42'


def test_error_saved_in_checklist_is_used_on_next_feedback(client,live,monkeypatch):
    t=final(start(client))
    r=client.put('/api/tickets/'+t['ticket_id']+'/information',json={'version':t['version'],'information':{'error_code':'E42'}})
    assert r.status_code==200
    t=r.json()
    calls=[];original=W.retrieve
    def retrieve(*args,**kwargs): calls.append(args[1]);return original(*args,**kwargs)
    monkeypatch.setattr(W,'retrieve',retrieve)
    final(feedback(client,t,note='I saved the exact code in the checklist. hybrid still fails.'))
    assert calls and 'E42' in calls[0]
