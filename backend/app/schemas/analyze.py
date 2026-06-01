from pydantic import BaseModel, HttpUrl
from app.models.domain import Video

class AnalyzeRequest(BaseModel):
    youtube_url: str
    instagram_url: str

class AnalyzeResponse(BaseModel):
    videoA: Video
    videoB: Video
    status: str = "completed"
