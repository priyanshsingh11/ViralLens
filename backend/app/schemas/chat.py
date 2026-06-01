from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str
    content: str

class Citation(BaseModel):
    source_id: str
    timestamp: float
    text: str

class ChatRequest(BaseModel):
    video_id: str
    messages: List[ChatMessage]

class ChatResponse(BaseModel):
    messages: List[ChatMessage]
    citations: Optional[List[Citation]] = None
