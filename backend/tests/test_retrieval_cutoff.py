import pytest
from fastapi import HTTPException
from test_api import client, providers, configure, add_doc, main
from test_tickets import ticket


@pytest.mark.parametrize('mode,rerank,score', [('vector',False,.8),('vector',True,.99),('hybrid',False,2/61)])
def test_cutoff_uses_final_score_including_equality(client,providers,mode,rerank,score):
    configure(client);doc=add_doc(client);main.ingest(doc)
    body={'query':'hybrid','mode':mode,'rerank':rerank,'min_score':score}
    result=client.post('/api/search',json=body).json()
    assert len(result['results'])==1
    assert result['min_score']==score
    result=client.post('/api/search',json={**body,'min_score':score+.0001}).json()
    assert result['results']==[]
    assert result['reranked']==rerank


def test_bm25_cutoff_has_its_own_scale(client,providers):
    configure(client);doc=add_doc(client);main.ingest(doc)
    body={'query':'hybrid','mode':'lexical','rerank':False}
    result=client.post('/api/search',json=body).json()
    score=result['results'][0]['score']
    assert result['score_type']=='BM25'
    assert client.post('/api/search',json={**body,'min_score':score*2}).json()['results']==[]
    assert client.post('/api/search',json={**body,'min_score':100}).status_code==200
    assert client.post('/api/search',json={**body,'mode':'vector','min_score':2}).status_code==422


def test_env_cutoff_applies_to_workflow_and_old_evidence_is_removed(client,providers,monkeypatch):
    configure(client);doc=add_doc(client);main.ingest(doc)
    t=ticket(client)
    W=main.ticket_workflow
    W.retrieve(t,'hybrid','vector')
    assert t['workflow']['evidence']
    monkeypatch.setenv('RETRIEVAL_VECTOR_MIN_SCORE','0.9')
    main.live_workflow.prune_evidence(t,None)
    assert t['workflow']['evidence']==[]
    trace=W.retrieve(t,'hybrid','vector')
    assert trace['min_score']==.9 and trace['matches']==0
    assert t['workflow']['evidence']==[]


def test_limits_are_taken_from_env_and_fail_without_configuration(client,providers,monkeypatch):
    configure(client)
    monkeypatch.setenv('CLAUDE_SUMMARY_MAX_TOKENS','1234')
    main.enrich(main.settings(),'Test document')
    assert providers[-1][1]['max_tokens']==1234
    monkeypatch.setenv('CLAUDE_HYDE_MAX_TOKENS','321')
    main.hypothetical_document(main.settings(),'Test query')
    assert providers[-1][1]['max_tokens']==321
    monkeypatch.delenv('CLAUDE_WORKFLOW_MAX_TOKENS')
    with pytest.raises(HTTPException,match='CLAUDE_WORKFLOW_MAX_TOKENS'):main.runtime_config.validate()
    monkeypatch.setenv('CLAUDE_WORKFLOW_MAX_TOKENS','NaN')
    with pytest.raises(HTTPException):main.runtime_config.validate()
