import pytest
from app.services.pipeline.processor import TranscriptProcessor
from app.services.pipeline.chunking import ChunkingService

def test_processor_cleans_text():
    processor = TranscriptProcessor()
    raw = "Hello   world! \n\n This is a [Music] test."
    cleaned = processor.clean_text(raw)
    assert cleaned == "Hello world! This is a test."

def test_chunker_splits_text():
    chunker = ChunkingService(chunk_size=50, chunk_overlap=10)
    text = "This is a long sentence that should definitely be split up into multiple smaller chunks because the chunk size is very small."
    chunks = chunker.chunk_transcript(text, "video-123", "youtube")
    
    assert len(chunks) > 1
    assert chunks[0]["metadata"]["video_id"] == "video-123"
    assert chunks[0]["metadata"]["platform"] == "youtube"
    assert "chunk_index" in chunks[0]
    assert "text" in chunks[0]
