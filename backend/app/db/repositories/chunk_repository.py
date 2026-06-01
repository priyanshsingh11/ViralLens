from typing import List, Optional
from uuid import UUID
from app.db.repositories.base import BaseRepository
from app.models.domain import TranscriptChunk

class ChunkRepository(BaseRepository):
    def insert_chunk(self, chunk: TranscriptChunk) -> TranscriptChunk:
        data = chunk.model_dump(exclude_none=True)
        if "id" in data and isinstance(data["id"], UUID):
            data["id"] = str(data["id"])
        data["video_id"] = str(data["video_id"])
        
        response = self.client.table("transcript_chunks").insert(data).execute()
        return TranscriptChunk(**response.data[0])

    def insert_chunks_bulk(self, chunks: List[TranscriptChunk]) -> List[TranscriptChunk]:
        data = []
        for chunk in chunks:
            chunk_data = chunk.model_dump(exclude_none=True)
            if "id" in chunk_data and isinstance(chunk_data["id"], UUID):
                chunk_data["id"] = str(chunk_data["id"])
            chunk_data["video_id"] = str(chunk_data["video_id"])
            data.append(chunk_data)
            
        response = self.client.table("transcript_chunks").insert(data).execute()
        return [TranscriptChunk(**row) for row in response.data]

    def match_transcript_chunks(
        self, 
        query_embedding: List[float], 
        match_threshold: float = 0.5, 
        match_count: int = 5, 
        filter_video_id: Optional[str | UUID] = None
    ) -> List[dict]:
        """
        Calls the PostgreSQL RPC function 'match_transcript_chunks' 
        to perform a vector similarity search using pgvector.
        """
        params = {
            "query_embedding": query_embedding,
            "match_threshold": match_threshold,
            "match_count": match_count
        }
        if filter_video_id:
            params["filter_video_id"] = str(filter_video_id)
            
        response = self.client.rpc("match_transcript_chunks", params).execute()
        return response.data
