import pytest
from uuid import uuid4
from app.services.retrieval.retrieval_service import RetrievalService

class MockQueryEmbedder:
    def embed_query(self, query):
        return [0.1] * 1536

class MockRetrievalRepo:
    def __init__(self, raw_results):
        self.raw_results = raw_results
    
    def similarity_search(self, query_embedding, top_k, video_ids):
        return self.raw_results

def test_retrieval_deduplication_and_formatting(monkeypatch):
    from app.core.config import settings
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "test_key")
    monkeypatch.setattr(settings, "SUPABASE_URL", "http://test")
    monkeypatch.setattr(settings, "SUPABASE_SERVICE_ROLE_KEY", "test_key")
    
    vid1 = uuid4()
    raw_results = [
        {"id": "chunk1", "video_id": str(vid1), "chunk_index": 0, "chunk_text": "hello", "similarity": 0.95},
        {"id": "chunk1", "video_id": str(vid1), "chunk_index": 0, "chunk_text": "hello", "similarity": 0.95}, # Duplicate
        {"id": "chunk2", "video_id": str(vid1), "chunk_index": 1, "chunk_text": "world", "similarity": 0.85},
    ]

    service = RetrievalService()
    service.query_embedder = MockQueryEmbedder()
    service.retrieval_repo = MockRetrievalRepo(raw_results)
    
    result = service.retrieve_context("test query", top_k=5)
    
    # Should deduplicate chunk1
    assert len(result["results"]) == 2
    
    # Should format citation correctly
    assert result["results"][0]["citation"] == f"[{vid1} Chunk 0]"
    
    # Should rank by score descending
    assert result["results"][0]["score"] > result["results"][1]["score"]
