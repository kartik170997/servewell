import json
import pytest
from test_api import client, providers, main
from test_live_workflow import live, start, final, feedback


def test_real_mlflow_persists_graph_runs_traces_and_artifacts(client,live,tmp_path,monkeypatch):
    import mlflow
    from mlflow import MlflowClient
    O=main.observability
    uri='sqlite:///'+(tmp_path/'tracking.db').as_posix()
    mc=MlflowClient(tracking_uri=uri)
    experiment=mc.create_experiment('workflow-integration',artifact_location=(tmp_path/'artifacts').as_uri())
    monkeypatch.setenv('MLFLOW_ENABLED','true')
    monkeypatch.setenv('MLFLOW_TRACKING_URI',uri)
    monkeypatch.setenv('MLFLOW_EXPERIMENT_NAME','workflow-integration')
    monkeypatch.setenv('MLFLOW_ENABLE_ASYNC_TRACE_LOGGING','false')
    monkeypatch.setenv('MLFLOW_DISABLE_TELEMETRY','true')
    monkeypatch.setattr(O,'_CONFIG',None);monkeypatch.setattr(O,'_LAST_FAILURE',0)
    t=final(start(client))
    runs=mc.search_runs([experiment])
    assert len(runs)==1 and runs[0].info.status=='FINISHED'
    run=runs[0]
    assert {a.path for a in mc.list_artifacts(run.info.run_id)}=={'logs','workflow'}
    trace=mlflow.get_trace(run.data.tags['trace_id'])
    names={span.name for span in trace.data.spans}
    assert {'workflow.query','graph.classify','graph.retrieve','graph.plan','graph.prepare'}<=names
    assert len(mlflow.search_traces(run_id=run.info.run_id,return_type='list'))==1
    assert trace.info.trace_metadata['mlflow.trace.session']==t['ticket_id']
    assert 'SECRET_CLAUDE' not in trace.to_json()
    assert 'SECRET_PINECONE' not in trace.to_json()
    t=final(feedback(client,t))
    assert len(mc.search_runs([experiment]))==1
    traces=mc.search_traces(locations=[experiment],max_results=20)
    assert len(traces)==1
    combined=mc.get_trace(run.data.tags['trace_id'])
    assert {'workflow.query','workflow.feedback','ticket.'+t['ticket_id']}<={s.name for s in combined.data.spans}
    # Reinitialize local identity storage as a restarted backend would.
    O.ticket_tracing.initialize(main.DATA)
    t=final(feedback(client,t))
    assert len(mc.search_runs([experiment]))==1
    assert len(mc.search_traces(locations=[experiment],max_results=20))==1
    combined=mc.get_trace(run.data.tags['trace_id'])
    assert len([s for s in combined.data.spans if s.name=='workflow.feedback'])==2
    roots=[s for s in combined.data.spans if s.parent_id is None]
    assert len(roots)==1 and roots[0].name=='ticket.'+t['ticket_id']
    assert all(s.parent_id==roots[0].span_id for s in combined.data.spans if s.name.startswith('workflow.'))
    assert any(a.path=='logs/turns/000001.json' for a in mc.list_artifacts(run.info.run_id,'logs/turns'))

    @O.stream_operation
    def retryable_failure(ticket_id,kind,body):
        with O.span('test.model','LLM'):
            O.model_usage({'test-model':{'prompt_tokens':10,'completion_tokens':2,'total_tokens':12,
                                       'cache_read_input_tokens':8}})
        yield {'type':'error','message':'Retry this operation'}
    list(retryable_failure(t['ticket_id'],'recover',{}))
    list(retryable_failure(t['ticket_id'],'recover',{}))
    assert len(mc.search_traces(locations=[experiment],max_results=20))==1
    combined=mc.get_trace(run.data.tags['trace_id'])
    usage=json.loads(combined.info.trace_metadata['mlflow.trace.tokenUsage'])
    assert usage['total_tokens']==24
    assert len([s for s in combined.data.spans if s.name=='workflow.recover' and s.status.status_code.value=='ERROR'])==2
    assert mc.get_run(run.info.run_id).info.status=='FAILED'
    assert O._RUN.get() is None and O._SUPPRESS.get() is False

    dataset=mlflow.genai.create_dataset(name='test-golden',experiment_id=experiment)
    dataset.merge_records([{'inputs':{'case_id':'test','query':'Test query'},'expectations':{'should_escalate':False}}])
    assert len(dataset.to_df())==1
