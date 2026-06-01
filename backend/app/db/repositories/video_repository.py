from typing import Optional
from uuid import UUID
from app.db.repositories.base import BaseRepository
from app.models.domain import Video

class VideoRepository(BaseRepository):
    def insert_video(self, video: Video) -> Video:
        data = video.model_dump(exclude_none=True)
        # Convert UUIDs to strings for JSON serialization
        if "id" in data and isinstance(data["id"], UUID):
            data["id"] = str(data["id"])
            
        response = self.client.table("videos").insert(data).execute()
        return Video(**response.data[0])

    def get_video_by_url(self, url: str) -> Optional[Video]:
        response = self.client.table("videos").select("*").eq("url", url).execute()
        if response.data:
            return Video(**response.data[0])
        return None
        
    def get_video_by_id(self, video_id: str | UUID) -> Optional[Video]:
        response = self.client.table("videos").select("*").eq("id", str(video_id)).execute()
        if response.data:
            return Video(**response.data[0])
        return None
