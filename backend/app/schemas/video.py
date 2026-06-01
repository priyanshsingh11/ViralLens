from pydantic import BaseModel
from typing import Optional

class VideoMetadata(BaseModel):
    id: str
    title: str
    url: str
    duration_seconds: Optional[int] = None
    processed: bool = False
