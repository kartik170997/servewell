import json
import sys
from types import SimpleNamespace
import pytest
import observability as O
from import_golden import read_records


def test_sensitive_fields_and_embedded_credentials_are_redacted():
    O.register_secrets('WORKSPACE_SECRET_EXAMPLE')
    value=O.sanitize({'x-api-key':'raw-secret','claude_key':'saved-secret','query':'WORKSPACE_SECRET_EXAMPLE Bearer another-secret','usage':{'total_tokens':12}})
    assert 'secret' not in json.dumps(value).lower()
    assert value['usage']['total_tokens']==12


def test_trace_preserves_error_without_exporting_raw_exception(monkeypatch):
    saved={}
    class Span:
        trace_id='trace-test'
        def set_inputs(self,x): saved['inputs']=x
        def set_attributes(self,x): saved.update(x)
        def set_outputs(self,x): saved['outputs']=x
        def set_status(self,x): saved['status']=x
    class Manager:
        def __enter__(self): return Span()
        def __exit__(self,*args): saved['exit']=args
    monkeypatch.setattr(O,'configure',lambda:True)
    monkeypatch.setitem(sys.modules,'mlflow',SimpleNamespace(start_span=lambda **kw:Manager()))
    @O.traced('test')
    def fail(api_key): raise RuntimeError('SECRET-IN-EXCEPTION')
    with pytest.raises(RuntimeError): fail('SECRET-KEY')
    assert saved['status']=='ERROR' and saved['exit']==(None,None,None)
    assert 'SECRET' not in json.dumps(saved)


def test_telemetry_outage_does_not_break_workflow(monkeypatch):
    monkeypatch.setattr(O,'configure',lambda:True)
    def unavailable(**kw): raise ConnectionError('offline')
    monkeypatch.setitem(sys.modules,'mlflow',SimpleNamespace(start_span=unavailable))
    @O.traced('test')
    def answer(): return 42
    assert answer()==42


def test_golden_validation_rejects_unreviewed_examples_and_duplicates(tmp_path):
    path=tmp_path/'cases.jsonl'
    row={'inputs':{'case_id':'1','query':'A question'},'expectations':{'should_escalate':False}}
    path.write_text(json.dumps(row))
    assert read_records(path)==[row]
    path.write_text(json.dumps(row)+'\n'+json.dumps(row))
    with pytest.raises(ValueError,match='unique'): read_records(path)
    row['tags']={'status':'example-only-not-reviewed'};path.write_text(json.dumps(row))
    with pytest.raises(ValueError,match='reviewed'): read_records(path)


def test_ticket_trace_identity_outage_does_not_break_workflow(monkeypatch):
    monkeypatch.setattr(O,'configure',lambda:True)
    def unavailable(*args): raise ConnectionError('offline')
    monkeypatch.setattr(O.ticket_tracing,'begin',unavailable)
    @O.stream_operation
    def operation(ticket_id,kind,body):
        yield {'type':'stage','node':'classify','message':'Checking'}
        raise ValueError('A failed model decision')
    with pytest.raises(ValueError): list(operation('WF-test','query',{'query':'Test'}))
    assert O._RUN.get() is None
    assert O._SUPPRESS.get() is False


def test_model_signature_class_is_serialized_without_calling_model_dump():
    from pydantic import BaseModel
    class Signature(BaseModel): pass
    assert O.sanitize({'signature':Signature})=={'signature':'Signature'}
