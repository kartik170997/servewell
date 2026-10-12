"""Validated provider and retrieval configuration. Values come only from the environment."""
import math
import os
from fastapi import HTTPException

INTEGER_SETTINGS = {
    'CLAUDE_SUMMARY_MAX_TOKENS': (1, 200000),
    'CLAUDE_HYDE_MAX_TOKENS': (1, 200000),
    'CLAUDE_WORKFLOW_MAX_TOKENS': (1, 200000),
    'CLAUDE_LEGACY_MAX_TOKENS': (1, 200000),
    'PROVIDER_TIMEOUT_SECONDS': (1, 600),
    'PROVIDER_MAX_ATTEMPTS': (1, 10),
    'WORKFLOW_MODEL_MAX_RETRIES': (0, 10),
    'WORKFLOW_OUTPUT_MAX_RETRIES': (0, 3),
    'WORKFLOW_PLANNING_MAX_QUESTIONS': (1, 2),
    'WORKFLOW_RETRIEVAL_TOP_K': (1, 20),
    'WORKFLOW_RETRIEVAL_CANDIDATES': (5, 100),
}
CUTOFF_SETTINGS = {'Similarity':'RETRIEVAL_VECTOR_MIN_SCORE','Rerank':'RETRIEVAL_RERANK_MIN_SCORE',
                   'BM25':'RETRIEVAL_BM25_MIN_SCORE','RRF':'RETRIEVAL_RRF_MIN_SCORE'}


def number(name, integer=False, minimum=0, maximum=None):
    try:
        raw=os.environ[name].strip()
        value=int(raw) if integer else float(raw)
        if not math.isfinite(value) or value<minimum or (maximum is not None and value>maximum): raise ValueError()
        return value
    except (KeyError,ValueError,OverflowError):
        raise HTTPException(503,f'Set a valid {name} in .env and restart the backend.') from None


def integer(name):
    low,high=INTEGER_SETTINGS[name]
    return number(name,True,low,high)


def cutoffs():
    return {kind:number(name,maximum=None if kind=='BM25' else 1) for kind,name in CUTOFF_SETTINGS.items()}


def boolean(name):
    value=os.getenv(name,'').strip().lower()
    if value not in ('true','false'): raise HTTPException(503,f'Set {name}=true or false in .env.')
    return value=='true'


def cache_ttl():
    value=os.getenv('PROCEDURE_CACHE_TTL','').strip()
    if value not in ('5m','1h'): raise HTTPException(503,'Set PROCEDURE_CACHE_TTL to 5m or 1h in .env.')
    return value


def validate():
    for name in INTEGER_SETTINGS: integer(name)
    cutoffs()
    cache_ttl()
    boolean('WORKFLOW_RETRIEVAL_RERANK')
    if integer('WORKFLOW_RETRIEVAL_CANDIDATES')<integer('WORKFLOW_RETRIEVAL_TOP_K'):
        raise HTTPException(503,'WORKFLOW_RETRIEVAL_CANDIDATES must be at least WORKFLOW_RETRIEVAL_TOP_K.')
