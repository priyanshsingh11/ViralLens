import yt_dlp
from typing import Dict, Any
from datetime import datetime, timezone
import re
from youtube_transcript_api import YouTubeTranscriptApi
from app.services.extractors.base import BaseExtractor
from app.models.domain import Video
from app.core.errors import ExtractionError, InvalidUrlError

class YoutubeExtractor(BaseExtractor):
    def validate_url(self, url: str) -> bool:
        pattern = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.be)\/.+$"
        return bool(re.match(pattern, url))

    def _extract_video_id(self, url: str) -> str:
        if "youtu.be" in url:
            return url.split("/")[-1].split("?")[0]
        if "v=" in url:
            return url.split("v=")[1].split("&")[0]
        
        # Handle shorts
        if "/shorts/" in url:
            return url.split("/shorts/")[1].split("?")[0]
            
        raise InvalidUrlError(url, "YouTube")

    def extract_metadata(self, url: str) -> Dict[str, Any]:
        ydl_opts = {
            'quiet': True,
            'extract_flat': False,
            'skip_download': True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e:
            raise ExtractionError(f"yt-dlp extraction failed: {str(e)}", "YouTube")

    def extract_transcript(self, video_id: str) -> str:
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            full_text = " ".join([t['text'] for t in transcript_list])
            return full_text
        except Exception as e:
            return ""

    def get_video_data(self, url: str) -> Video:
        if not self.validate_url(url):
            raise InvalidUrlError(url, "YouTube")

        video_id = self._extract_video_id(url)
        metadata = self.extract_metadata(url)
        transcript = self.extract_transcript(video_id)

        upload_date = None
        if metadata.get('upload_date'):
            try:
                date_str = metadata['upload_date']
                upload_date = datetime.strptime(date_str, "%Y%m%d").replace(tzinfo=timezone.utc)
            except ValueError:
                pass
                
        views = metadata.get('view_count')
        likes = metadata.get('like_count')
        comments = metadata.get('comment_count')
        
        # Avoid division by zero and handle None values
        engagement_rate = None
        if views and views > 0:
            eng = (likes or 0) + (comments or 0)
            engagement_rate = (eng / views) * 100
            
        # Ensure engagement_rate is a float with precision matched if needed
        if engagement_rate is not None:
            engagement_rate = round(engagement_rate, 4)

        return Video(
            platform="youtube",
            url=url,
            creator_name=metadata.get('uploader'),
            creator_followers=metadata.get('channel_follower_count'),
            views=views,
            likes=likes,
            comments=comments,
            engagement_rate=engagement_rate,
            upload_date=upload_date,
            duration_seconds=metadata.get('duration'),
            transcript=transcript or metadata.get('description') # Fallback to description if no transcript
        )
