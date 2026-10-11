import json
import sqlite3

import dspy
import pytest
import main
import live_workflow as L
from test_api import client, providers, configure, add_doc
from test_tickets import ticket


def test_procedure_revisions_are_immutable_and_tickets_pinned(client):
    original=client.get('/api/procedures').json()['active']
    old=ticket(client)
    changed=client.post('/api/procedures',json={'expected_version':1,'text':original['text']+'\nRevision test.','note':'Test revision'})
    assert changed.status_code==201
    assert changed.json()['version']==2
    assert changed.json()['sha256']!=original['sha256']
    assert client.get('/api/procedures/1').json()==original
    assert client.get('/api/tickets/'+old['ticket_id']).json()['procedure_ref']['version']==1
    new=ticket(client,ticket_id='INC-NEW')
    assert new['procedure_ref']['version']==2
    assert main.ticket_workflow.procedure_for(old)['text']==original['text']
    assert client.post('/api/procedures',json={'expected_version':1,'text':original['text'],'note':'Stale edit'}).status_code==409
    with pytest.raises(sqlite3.IntegrityError),main.db() as c:
        c.execute('UPDATE procedure_versions SET text=? WHERE version=1',('Overwrite',))
    main.initialize()
    assert client.get('/api/procedures').json()['active']['version']==2


def test_revision_retrieval_and_deleted_audit(client,providers):
    configure(client)
    first=add_doc(client);main.ingest(first)
    second=add_doc(client,content=b'Changed handbook about hybrid retrieval.')
    def search():
        return client.post('/api/search',json={'query':'hybrid','mode':'lexical','rerank':False}).json()['results']
    assert {r['document_id'] for r in search()}=={first}  # Pending replacement preserves ready source.
    main.ingest(second)
    results=search()
    assert {r['document_id'] for r in results}=={second}
    assert results[0]['document_version']==2
    assert len(results[0]['content_sha256'])==64
    history=client.get('/api/documents/'+second+'/versions').json()['versions']
    assert [v['document_version'] for v in history]==[2,1]
    assert history[0]['lineage_id']==history[1]['lineage_id']
    assert client.get('/api/documents/'+first+'/download').status_code==200
    assert add_doc(client,content=b'Changed handbook about hybrid retrieval.')==second
    assert client.delete('/api/documents/'+second).status_code==200
    assert client.get('/api/documents/'+second+'/versions').json()['versions'][0]['deleted_at']
    assert search()[0]['document_id']==first


def test_cache_prefix_stable_across_signatures_and_inputs(client,monkeypatch):
    monkeypatch.setenv('PROCEDURE_CACHE_TTL','1h')
    p=main.versioning.procedure(main)
    adapter=L.ProcedureChatAdapter(p)
    a=adapter.format(dspy.Signature('procedure, context -> answer'),[],{'procedure':p['text'],'context':'First'})
    b=adapter.format(dspy.Signature('procedure, context -> decision'),[],{'procedure':p['text'],'context':'Second'})
    assert a[0]['content'][0]==b[0]['content'][0]
    assert a[0]['content'][0]['cache_control']=={'type':'ephemeral','ttl':'1h'}
    assert p['text'] not in json.dumps(a[1:])
    assert a[0]['content'][1]!=b[0]['content'][1]


def test_migration_preserves_existing_data_and_marks_unknown_history(client):
    t=ticket(client)
    with main.db() as c:
        t.pop('procedure_ref')
        c.execute('UPDATE tickets SET payload=? WHERE ticket_id=?',(json.dumps(t),t['ticket_id']))
        d={'id':'legacy','filename':'old.md','status':'ready','summary':'old summary','tags':[]}
        c.execute('INSERT INTO documents VALUES (?,?,?,?)',('legacy','legacy-hash','ready',json.dumps(d)))
    main.initialize();main.initialize()
    assert main.get_doc('legacy')['document_version']==1
    assert client.get('/api/tickets/'+t['ticket_id']).json()['procedure_ref']['assigned_on_upgrade']
    assert len(client.get('/api/documents/legacy/versions').json()['versions'])==1
