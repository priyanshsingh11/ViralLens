import logging
from typing import Dict, Any
from uuid import UUID
from app.services.pipeline.processor import TranscriptProcessor
from app.services.pipeline.chunking import ChunkingService
from app.services.pipeline.embedding import EmbeddingService
from app.db.repositories.chunk_repository import ChunkRepository
from app.models.domain import TranscriptChunk

logger = logging.getLogger(__name__)

class TranscriptEmbeddingPipeline:
    def __init__(self):
        self.processor = TranscriptProcessor()
        self.chunker = ChunkingService()
        self.embedder = EmbeddingService()
        self.chunk_repo = ChunkRepository()

    def process_video_transcript(self, video_id: UUID | str, transcript: str, platform: str) -> Dict[str, Any]:
        logger.info(f"Starting transcript pipeline for video {video_id}")
        
        # 1. Clean transcript
        clean_text = self.processor.clean_text(transcript)
        if not clean_text:
            logger.warning(f"No transcript text available after cleaning for video {video_id}")
            return {
                "video_id": str(video_id),
                "chunks_created": 0,
                "embeddings_generated": 0,
                "status": "success - no transcript"
            }
            
        logger.info("Transcript cleaned")
        
        # 2. Chunk transcript
        chunks_data = self.chunker.chunk_transcript(clean_text, str(video_id), platform)
        logger.info(f"{len(chunks_data)} chunks generated")
        
        if not chunks_data:
            return {
                "video_id": str(video_id),
                "chunks_created": 0,
                "embeddings_generated": 0,
                "status": "success - zero chunks"
            }

        # 3. Generate embeddings
        texts = [c["text"] for c in chunks_data]
        embeddings = self.embedder.generate_batch_embeddings(texts)
        logger.info(f"{len(embeddings)} embeddings generated")

        # 4. Store in database
        chunk_models = []
        for i, chunk_data in enumerate(chunks_data):
            chunk_models.append(
                TranscriptChunk(
                    video_id=video_id,
                    chunk_index=chunk_data["chunk_index"],
                    chunk_text=chunk_data["text"],
                    embedding=embeddings[i]
                )
            )
            
        self.chunk_repo.insert_chunks_bulk(chunk_models)
        logger.info(f"Embeddings and chunks stored in Supabase successfully for {video_id}")

        return {
            "video_id": str(video_id),
            "chunks_created": len(chunks_data),
            "embeddings_generated": len(embeddings),
            "status": "success"
        }
