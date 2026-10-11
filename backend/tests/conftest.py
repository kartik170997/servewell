import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pytest

@pytest.fixture(autouse=True)
def configured_models(monkeypatch):
    monkeypatch.setenv('MLFLOW_ENABLED','false')
    # Tests must never depend on the developer's model selections.
    monkeypatch.setenv('CLAUDE_MODEL', 'test-claude')
    monkeypatch.setenv('EMBEDDING_MODEL', 'test-embedding')
    monkeypatch.setenv('RERANK_MODEL', 'test-reranker')
