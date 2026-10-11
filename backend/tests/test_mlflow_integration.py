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
    assert trace.info.trace_metadata['mlflow.sourceRun']==run.info.run_id
    assert trace.info.trace_metadata['mlflow.trace.session']==t['ticket_id']
    assert 'SECRET_CLAUDE' not in trace.to_json()
    assert 'SECRET_PINECONE' not in trace.to_json()
    t=final(feedback(client,t))
    assert len(mc.search_runs([experiment]))==2

    dataset=mlflow.genai.create_dataset(name='test-golden',experiment_id=experiment)
    dataset.merge_records([{'inputs':{'case_id':'test','query':'Test query'},'expectations':{'should_escalate':False}}])
    assert len(dataset.to_df())==1
