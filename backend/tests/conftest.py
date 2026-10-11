import pytest

@pytest.fixture(autouse=True)
def configured_models(monkeypatch):
    # Tests must never depend on the developer's model selections.
    monkeypatch.setenv('CLAUDE_MODEL', 'test-claude')
    monkeypatch.setenv('EMBEDDING_MODEL', 'test-embedding')
    monkeypatch.setenv('RERANK_MODEL', 'test-reranker')
