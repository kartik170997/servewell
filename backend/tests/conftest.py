import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pytest

@pytest.fixture(autouse=True)
def configured_models(monkeypatch):
    monkeypatch.setenv('MLFLOW_ENABLED','false')
    monkeypatch.setenv('PROCEDURE_CACHE_TTL','1h')
    # Tests must never depend on the developer's model selections.
    monkeypatch.setenv('CLAUDE_MODEL', 'test-claude')
    monkeypatch.setenv('EMBEDDING_MODEL', 'test-embedding')
    monkeypatch.setenv('RERANK_MODEL', 'test-reranker')

    # Independent of local generation limits and score tuning.
    monkeypatch.setenv('CLAUDE_SUMMARY_MAX_TOKENS', '2200')
    monkeypatch.setenv('CLAUDE_HYDE_MAX_TOKENS', '600')
    monkeypatch.setenv('CLAUDE_WORKFLOW_MAX_TOKENS', '15000')
    monkeypatch.setenv('CLAUDE_LEGACY_MAX_TOKENS', '2200')
    monkeypatch.setenv('PROVIDER_TIMEOUT_SECONDS', '90')
    monkeypatch.setenv('PROVIDER_MAX_ATTEMPTS', '3')
    monkeypatch.setenv('WORKFLOW_MODEL_MAX_RETRIES', '1')
    monkeypatch.setenv('RETRIEVAL_VECTOR_MIN_SCORE', '0.5')
    monkeypatch.setenv('RETRIEVAL_RERANK_MIN_SCORE', '0.3')
    monkeypatch.setenv('RETRIEVAL_BM25_MIN_SCORE', '0')
    monkeypatch.setenv('RETRIEVAL_RRF_MIN_SCORE', '0.01')
    monkeypatch.setenv('WORKFLOW_RETRIEVAL_TOP_K', '5')
    monkeypatch.setenv('WORKFLOW_RETRIEVAL_CANDIDATES', '30')
    monkeypatch.setenv('WORKFLOW_RETRIEVAL_RERANK', 'false')
