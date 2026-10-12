"""Immutable procedure revisions and document lineage, stored alongside application data."""
import hashlib
import json
import os
from pathlib import Path

from fastapi import Depends, HTTPException
from pydantic import BaseModel, Field
if __package__:
    from . import privacy
else:
    import privacy

PROCEDURE_ID = 'SOP-IT-L1-002'


def ref(p):
    return {k: p[k] for k in ('id', 'version', 'sha256')}


def initialize(a):
    with a.db() as c:
        c.executescript('''
        CREATE TABLE IF NOT EXISTS procedure_versions (
            id TEXT NOT NULL, version INTEGER NOT NULL, sha256 TEXT NOT NULL,
            text TEXT NOT NULL, created_at TEXT NOT NULL, note TEXT NOT NULL,
            PRIMARY KEY(id,version));
        CREATE TABLE IF NOT EXISTS procedure_heads (id TEXT PRIMARY KEY, version INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS document_versions (
            document_id TEXT PRIMARY KEY, lineage_id TEXT NOT NULL, version INTEGER NOT NULL,
            filename TEXT NOT NULL, sha256 TEXT NOT NULL, payload TEXT NOT NULL,
            deleted_at TEXT, UNIQUE(lineage_id,version));
        CREATE TRIGGER IF NOT EXISTS immutable_procedure_update BEFORE UPDATE ON procedure_versions
            BEGIN SELECT RAISE(ABORT,'Procedure revisions are immutable'); END;
        CREATE TRIGGER IF NOT EXISTS immutable_procedure_delete BEFORE DELETE ON procedure_versions
            BEGIN SELECT RAISE(ABORT,'Procedure revisions are immutable'); END;
        ''')
        if not c.execute('SELECT 1 FROM procedure_heads WHERE id=?', (PROCEDURE_ID,)).fetchone():
            text = Path(__file__).with_name('escalation_procedure.md').read_text(encoding='utf-8')
            c.execute('INSERT INTO procedure_versions VALUES (?,?,?,?,?,?)',
                      (PROCEDURE_ID, 1, hashlib.sha256(text.encode()).hexdigest(), text, a.now(), 'Initial Markdown import'))
            c.execute('INSERT INTO procedure_heads VALUES (?,1)', (PROCEDURE_ID,))
        for r in c.execute('SELECT * FROM documents ORDER BY rowid').fetchall():
            if not c.execute('SELECT 1 FROM document_versions WHERE document_id=?', (r['id'],)).fetchone():
                d = json.loads(r['payload'])
                register_document(c, d, r['hash'])
                c.execute('UPDATE documents SET payload=? WHERE id=?', (json.dumps(d), r['id']))
        p = dict(c.execute('SELECT v.* FROM procedure_versions v JOIN procedure_heads h USING(id,version)').fetchone())
        for r in c.execute('SELECT ticket_id,payload FROM tickets').fetchall():
            t = json.loads(r['payload'])
            if 'procedure_ref' not in t:
                t['procedure_ref'] = {**ref(p), 'assigned_on_upgrade': True}
                c.execute('UPDATE tickets SET payload=? WHERE ticket_id=?', (json.dumps(t), r['ticket_id']))


def procedure(a, reference=None):
    with a.db() as c:
        if reference:
            row = c.execute('SELECT * FROM procedure_versions WHERE id=? AND version=?',
                            (reference['id'], reference['version'])).fetchone()
        else:
            row = c.execute('SELECT v.* FROM procedure_versions v JOIN procedure_heads h USING(id,version) WHERE id=?', (PROCEDURE_ID,)).fetchone()
    if not row: raise HTTPException(404, 'Procedure version not found.')
    p = dict(row)
    if reference and reference.get('sha256') != p['sha256']:
        raise HTTPException(409, 'Procedure version checksum mismatch.')
    return p


def cache_block(p):
    ttl = os.getenv('PROCEDURE_CACHE_TTL', '1h')
    if ttl not in ('5m', '1h'): raise ValueError('PROCEDURE_CACHE_TTL must be 5m or 1h.')
    return {'type': 'text', 'text': f"Escalation procedure {p['id']} version {p['version']} SHA256 {p['sha256']}\n{privacy.mask_text(p['text'])}",
            'cache_control': {'type': 'ephemeral', 'ttl': ttl}}


def register_document(c, d, digest):
    previous = c.execute('SELECT lineage_id,version FROM document_versions WHERE filename=? ORDER BY version DESC LIMIT 1', (d['filename'],)).fetchone()
    d.update(lineage_id=previous['lineage_id'] if previous else d['id'],
             document_version=previous['version']+1 if previous else 1, content_sha256=digest)
    c.execute('INSERT INTO document_versions VALUES (?,?,?,?,?,?,NULL)',
              (d['id'],d['lineage_id'],d['document_version'],d['filename'],digest,json.dumps(d)))


def current_documents(docs):
    heads = {}
    for d in docs:
        key = d.get('lineage_id', d['id'])
        if key not in heads or d.get('document_version', 1) > heads[key].get('document_version', 1): heads[key] = d
    return list(heads.values())


class Revision(BaseModel):
    expected_version: int = Field(ge=1)
    text: str = Field(min_length=100, max_length=100000)
    note: str = Field(min_length=1, max_length=1000)


def install(a):
    auth = [Depends(a.auth)]

    @a.app.get('/api/procedures', dependencies=auth)
    def procedures():
        p = procedure(a)
        with a.db() as c:
            versions = [dict(r) for r in c.execute('SELECT id,version,sha256,created_at,note FROM procedure_versions WHERE id=? ORDER BY version DESC', (PROCEDURE_ID,))]
        return {'active': p, 'versions': versions, 'cache_ttl': os.getenv('PROCEDURE_CACHE_TTL', '1h')}

    @a.app.get('/api/procedures/{version}', dependencies=auth)
    def get_revision(version: int):
        with a.db() as c:
            r = c.execute('SELECT * FROM procedure_versions WHERE id=? AND version=?', (PROCEDURE_ID,version)).fetchone()
        if not r: raise HTTPException(404, 'Procedure version not found.')
        return dict(r)

    @a.app.post('/api/procedures', dependencies=auth, status_code=201)
    def revise(body: Revision):
        with a.MUTEX, a.db() as c:
            c.execute('BEGIN IMMEDIATE')
            current = c.execute('SELECT version FROM procedure_heads WHERE id=?', (PROCEDURE_ID,)).fetchone()['version']
            if current != body.expected_version: raise HTTPException(409, 'Procedure changed. Refresh before saving.')
            digest = hashlib.sha256(body.text.encode()).hexdigest()
            c.execute('INSERT INTO procedure_versions VALUES (?,?,?,?,?,?)', (PROCEDURE_ID,current+1,digest,body.text,a.now(),body.note))
            c.execute('UPDATE procedure_heads SET version=? WHERE id=?', (current+1,PROCEDURE_ID))
        return procedure(a)

    @a.app.get('/api/documents/{doc_id}/versions', dependencies=auth)
    def document_versions(doc_id: str):
        with a.db() as c:
            row = c.execute('SELECT lineage_id FROM document_versions WHERE document_id=?', (doc_id,)).fetchone()
            if not row: raise HTTPException(404, 'Document history not found.')
            return {'versions': [{**json.loads(r['payload']), 'deleted_at': r['deleted_at']} for r in c.execute('SELECT payload,deleted_at FROM document_versions WHERE lineage_id=? ORDER BY version DESC', (row['lineage_id'],))]}
