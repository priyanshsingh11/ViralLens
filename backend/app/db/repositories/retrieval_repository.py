import logging
from typing import List, Dict, Any, Optional
from uuid import UUID
from app.db.repositories.base import BaseRepository

logger = logging.getLogger(__name__)

class RetrievalRepository(BaseRepository):
    
    def similarity_search(self, query_embedding: List[float], top_k: int = 5, video_ids: Optional[List[UUID]] = None) -> List[Dict[str, Any]]:
        """
        Executes a native PostgreSQL pgvector cosine similarity search via RPC.
        Supports hybrid expansion by leaving space for keyword filters.
        """
        logger.info(f"Executing vector search (top_k={top_k})")
        
        filter_ids = [str(vid) for vid in video_ids] if video_ids else None
        
        response = self.client.rpc(
            'match_transcript_chunks', 
            {
                'query_embedding': query_embedding,
                'match_threshold': 0.0,
                'match_count': top_k,
                'filter_video_ids': filter_ids
            }
        ).execute()
        
        return response.data

    def search_video_chunks(self, query_embedding: List[float], video_id: UUID, top_k: int = 5) -> List[Dict[str, Any]]:
        return self.similarity_search(query_embedding, top_k=top_k, video_ids=[video_id])

    def search_across_videos(self, query_embedding: List[float], video_ids: List[UUID], top_k: int = 5) -> List[Dict[str, Any]]:
        return self.similarity_search(query_embedding, top_k=top_k, video_ids=video_ids)
