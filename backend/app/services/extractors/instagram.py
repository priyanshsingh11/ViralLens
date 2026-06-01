import instaloader
import re
from typing import Dict, Any
from datetime import datetime, timezone
from app.services.extractors.base import BaseExtractor
from app.models.domain import Video
from app.core.errors import ExtractionError, InvalidUrlError

class InstagramExtractor(BaseExtractor):
    def __init__(self):
        self.loader = instaloader.Instaloader(quiet=True)

    def validate_url(self, url: str) -> bool:
        pattern = r"^(https?\:\/\/)?(www\.)?instagram\.com\/(p|reel|reels)\/.+$"
        return bool(re.match(pattern, url))

    def _extract_shortcode(self, url: str) -> str:
        try:
            # Usually https://www.instagram.com/reel/SHORTCODE/
            # or https://instagram.com/p/SHORTCODE/
            # Strip query params
            clean_url = url.split("?")[0].strip("/")
            return clean_url.split("/")[-1]
        except IndexError:
            raise InvalidUrlError(url, "Instagram")

    def extract_metadata(self, url: str) -> Dict[str, Any]:
        shortcode = self._extract_shortcode(url)
        try:
            post = instaloader.Post.from_shortcode(self.loader.context, shortcode)
            return {
                "owner_username": post.owner_username,
                "owner_followers": post.owner_profile.followers if post.owner_profile else None,
                "likes": post.likes,
                "comments": post.comments,
                "caption": post.caption,
                "hashtags": post.caption_hashtags,
                "upload_date": post.date_utc,
                "is_video": post.is_video,
                "duration": post.video_duration,
                "video_view_count": post.video_view_count
            }
        except Exception as e:
            raise ExtractionError(f"Instaloader extraction failed: {str(e)}", "Instagram")

    def get_video_data(self, url: str) -> Video:
        if not self.validate_url(url):
            raise InvalidUrlError(url, "Instagram")

        metadata = self.extract_metadata(url)
        
        views = metadata.get('video_view_count')
        likes = metadata.get('likes', 0)
        comments = metadata.get('comments', 0)
        
        # Avoid division by zero
        engagement_rate = None
        if views and views > 0:
            eng = (likes or 0) + (comments or 0)
            engagement_rate = round((eng / views) * 100, 4)
            
        upload_date = metadata.get('upload_date')
        if upload_date and upload_date.tzinfo is None:
            upload_date = upload_date.replace(tzinfo=timezone.utc)
            
        # Add hashtags to transcript/caption if available
        caption = metadata.get('caption') or ""
        hashtags = metadata.get('hashtags')
        if hashtags:
            caption += f"\nHashtags: {' '.join(['#'+h for h in hashtags])}"

        return Video(
            platform="instagram",
            url=url,
            creator_name=metadata.get('owner_username'),
            creator_followers=metadata.get('owner_followers'),
            views=views,
            likes=likes,
            comments=comments,
            engagement_rate=engagement_rate,
            upload_date=upload_date,
            duration_seconds=metadata.get('duration') and int(metadata.get('duration')),
            transcript=caption
        )
