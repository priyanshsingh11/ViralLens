from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class RetrieveRequest(BaseModel):
    question: str
    video_ids: Optional[List[UUID]] = None
    top_k: int = 5

class RetrievedChunk(BaseModel):
    video_id: UUID
    chunk_index: int
    score: float
    text: str
    citation: str

class RetrieveResponse(BaseModel):
    query: str
    results: List[RetrievedChunk]
