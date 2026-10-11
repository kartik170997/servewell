"""Fail-open MLflow runs, structured event logs and sanitized nested traces."""
import functools
import inspect
import json
import logging
import os
import re
import threading
import time
from contextlib import contextmanager
from contextvars import ContextVar

_LOCK=threading.Lock()
_CONFIG=None
_CLIENT=None
_EXPERIMENT=None
_LAST_FAILURE=0
_SECRETS=set()
_RUN=ContextVar('folio_mlflow_run',default=None)
LOG=logging.getLogger(__name__)


def register_secrets(*values):
    _SECRETS.update(str(v) for v in values if v and len(str(v))>=6)


def sanitize(value, depth=0):
    if depth>10: return '[depth limit]'
    if isinstance(value,type): return value.__name__
    if hasattr(value,'model_dump'): value=value.model_dump(mode='json')
    if isinstance(value,dict):
        return {str(k):('[redacted]' if re.search(r'(^|[_-])(api[_-]?key|key|token|authorization|password|secret)$',str(k),re.I) else sanitize(v,depth+1)) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [sanitize(v,depth+1) for v in value[:100]]
    if isinstance(value,str):
        for secret in tuple(_SECRETS): value=value.replace(secret,'[redacted]')
        value=re.sub(r'(?i)Bearer\s+[^\s"\']+', 'Bearer [redacted]',value)
        value=re.sub(r'sk-[A-Za-z0-9_-]{12,}', '[redacted]',value)
        return value[:24000]
    if value is None or isinstance(value,(bool,int,float)): return value
    return getattr(value,'__name__',type(value).__name__)


def configure():
    global _CONFIG,_CLIENT,_EXPERIMENT,_LAST_FAILURE
    if os.getenv('MLFLOW_ENABLED','false').lower()!='true': return False
    uri=os.getenv('MLFLOW_TRACKING_URI','').strip();name=os.getenv('MLFLOW_EXPERIMENT_NAME','').strip()
    if not uri or not name: return False
    if _CONFIG==(uri,name): return True
    if time.monotonic()-_LAST_FAILURE<30: return False
    with _LOCK:
        if _CONFIG==(uri,name): return True
        try:
            import mlflow
            from mlflow import MlflowClient
            for key,value in os.environ.items():
                if any(word in key for word in ('TOKEN','API_KEY','PASSWORD','SECRET')): register_secrets(value)
            mlflow.set_tracking_uri(uri)
            experiment=mlflow.set_experiment(name)
            _CLIENT=MlflowClient(tracking_uri=uri);_EXPERIMENT=experiment.experiment_id
            _CONFIG=(uri,name)
            return True
        except Exception as error:
            _LAST_FAILURE=time.monotonic()
            LOG.warning('MLflow unavailable (%s); workflow continues without telemetry.',type(error).__name__)
            return False


def safe(fn,*args,**kwargs):
    try: return fn(*args,**kwargs)
    except Exception as error:
        LOG.warning('MLflow write failed (%s); workflow continues.',type(error).__name__)


class Record:
    def __init__(self): self.outputs=None;self.attributes={};self.trace_id=None


@contextmanager
def span(name,kind='CHAIN',inputs=None,attributes=None):
    record=Record();manager=None;active=None
    if configure():
        try:
            import mlflow
            manager=mlflow.start_span(name=name,span_type=kind)
            active=manager.__enter__();record.trace_id=active.trace_id
            safe(active.set_inputs,sanitize(inputs))
            attrs={**(attributes or {})}
            if _RUN.get():
                attrs['folio.run_id']=_RUN.get()
                safe(mlflow.update_current_trace,metadata={'mlflow.sourceRun':_RUN.get()})
            if attributes and attributes.get('mlflow.trace.session'):
                safe(mlflow.update_current_trace,metadata={'mlflow.trace.session':attributes['mlflow.trace.session']})
            safe(active.set_attributes,sanitize(attrs))
        except Exception as error:
            LOG.warning('MLflow span unavailable (%s).',type(error).__name__)
            if manager and active: safe(manager.__exit__,None,None,None)
            manager=None;active=None
    try:
        yield record
    except BaseException as error:
        if active:
            safe(active.set_attributes,{'error.type':type(error).__name__,'error.http_status':getattr(error,'status_code',None)})
            if isinstance(error,ValueError): safe(active.set_attributes,{'error.message':sanitize(str(error))})
            safe(active.set_status,'ERROR')
        raise
    finally:
        if active:
            if record.outputs is not None: safe(active.set_outputs,sanitize(record.outputs))
            safe(active.set_attributes,sanitize(record.attributes))
        # Never hand an unsanitized exception/traceback to the exporter.
        if manager: safe(manager.__exit__,None,None,None)


def traced(name=None,kind='CHAIN'):
    def decorate(fn):
        @functools.wraps(fn)
        def wrapped(*args,**kwargs):
            inputs=dict(inspect.signature(fn).bind_partial(*args,**kwargs).arguments)
            with span(name or fn.__name__,kind,inputs) as record:
                result=fn(*args,**kwargs);record.outputs=result;return result
        return wrapped
    return decorate


def stream_operation(fn):
    @functools.wraps(fn)
    def wrapped(ticket_id,kind,body):
        run_id=None;events=[];result=None;failed=False;started=time.monotonic();token=None
        if configure():
            run=safe(_CLIENT.create_run,_EXPERIMENT,tags={'mlflow.runName':ticket_id+' / '+kind,'ticket_id':ticket_id,'operation':kind})
            if run:
                run_id=run.info.run_id;token=_RUN.set(run_id)
                for field in ('CLAUDE_MODEL','EMBEDDING_MODEL','RERANK_MODEL'):
                    safe(_CLIENT.log_param,run_id,field,os.getenv(field,''))
        try:
            with span('workflow.'+kind,'AGENT',{'ticket_id':ticket_id,'request':body}, {'mlflow.trace.session':ticket_id}) as trace:
                if trace.trace_id and run_id: safe(_CLIENT.set_tag,run_id,'trace_id',trace.trace_id)
                for event in fn(ticket_id,kind,body):
                    if event.get('type') in ('stage','error'): events.append(sanitize(event))
                    if event.get('type')=='result':
                        result=event['ticket']
                        trace.outputs={'ticket_id':ticket_id,'status':result['status'],'checkpoint':result['workflow'].get('checkpoint'),'pending':result['workflow'].get('pending')}
                    yield event
        except BaseException as error:
            failed=True;events.append({'type':'error','error_type':type(error).__name__,'http_status':getattr(error,'status_code',None)})
            raise
        finally:
            if run_id:
                safe(_CLIENT.log_metric,run_id,'duration_seconds',time.monotonic()-started)
                safe(_CLIENT.log_metric,run_id,'stage_events',len(events))
                safe(_CLIENT.log_dict,run_id,{'events':events},'logs/events.json')
                if result:
                    w=result['workflow']
                    safe(_CLIENT.log_dict,run_id,sanitize({'procedure_ref':result.get('procedure_ref'),'evidence':w.get('evidence'),'classification':w.get('classification'),'plan':w.get('plan'),'steps':w.get('steps'),'tool_and_retrieval_trace':w.get('trace'),'checkpoint':w.get('checkpoint')}),'workflow/result.json')
                    safe(_CLIENT.set_tag,run_id,'ticket_status',result['status'])
                    safe(_CLIENT.set_tag,run_id,'procedure_version',str(result.get('procedure_ref',{}).get('version','unknown')))
                    safe(_CLIENT.log_metric,run_id,'retrieved_sources',len(w.get('evidence',[])))
                    safe(_CLIENT.log_metric,run_id,'planned_steps',len(w.get('plan',[])))
                    safe(_CLIENT.log_metric,run_id,'escalated',int(result.get('escalation_flag',False)))
                safe(_CLIENT.set_terminated,run_id,status='FAILED' if failed else 'FINISHED')
            if token is not None: _RUN.reset(token)
    return wrapped


def model_usage(usage):
    if not usage or not configure(): return
    def record():
        import mlflow
        active=mlflow.get_current_active_span()
        if active:
            active.set_attribute('model.usage',sanitize(usage))
            entries=[v for v in usage.values() if isinstance(v,dict)]
            counts={'input_tokens':sum(v.get('prompt_tokens',v.get('input_tokens',0)) or 0 for v in entries),
                'output_tokens':sum(v.get('completion_tokens',v.get('output_tokens',0)) or 0 for v in entries),
                'total_tokens':sum(v.get('total_tokens',0) or 0 for v in entries)}
            active.set_attribute('mlflow.chat.tokenUsage',counts)
    safe(record)
