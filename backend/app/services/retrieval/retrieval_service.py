import logging
from typing import List, Dict, Any, Optional
from uuid import UUID
from app.services.retrieval.query_embedding import QueryEmbeddingService
from app.db.repositories.retrieval_repository import RetrievalRepository

logger = logging.getLogger(__name__)

class RetrievalService:
    def __init__(self):
        self.query_embedder = QueryEmbeddingService()
        self.retrieval_repo = RetrievalRepository()

    def retrieve_context(self, question: str, video_ids: Optional[List[UUID]] = None, top_k: int = 5) -> Dict[str, Any]:
        logger.info(f"Retrieving context for question: '{question}' across videos: {video_ids}")
        
        query_embedding = self.query_embedder.embed_query(question)
        
        raw_results = self.retrieval_repo.similarity_search(
            query_embedding=query_embedding,
            top_k=top_k,
            video_ids=video_ids
        )
        
        seen_chunk_ids = set()
        formatted_results = []
        
        for result in raw_results:
            if result['id'] in seen_chunk_ids:
                continue
            seen_chunk_ids.add(result['id'])
            
            citation = f"[{result['video_id']} Chunk {result['chunk_index']}]"
            
            formatted_results.append({
                "video_id": result['video_id'],
                "chunk_index": result['chunk_index'],
                "score": result['similarity'],
                "text": result['chunk_text'],
                "citation": citation
            })
            
        formatted_results.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            "query": question,
            "results": formatted_results[:top_k]
        }
