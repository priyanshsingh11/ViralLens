from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class Video(BaseModel):
    id: Optional[UUID] = None
    platform: str
    url: str
    creator_name: Optional[str] = None
    creator_followers: Optional[int] = None
    views: Optional[int] = None
    likes: Optional[int] = None
    comments: Optional[int] = None
    engagement_rate: Optional[float] = None
    upload_date: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    transcript: Optional[str] = None
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class TranscriptChunk(BaseModel):
    id: Optional[UUID] = None
    video_id: UUID
    chunk_index: int
    chunk_text: str
    embedding: Optional[List[float]] = None
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class ChatSession(BaseModel):
    id: Optional[UUID] = None
    session_name: Optional[str] = None
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class ChatMessage(BaseModel):
    id: Optional[UUID] = None
    session_id: UUID
    role: str
    content: str
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class Citation(BaseModel):
    id: Optional[UUID] = None
    message_id: UUID
    video_id: UUID
    chunk_id: UUID
    
    model_config = ConfigDict(from_attributes=True)
