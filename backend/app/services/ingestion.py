import logging
from typing import Tuple
from fastapi import BackgroundTasks
from app.models.domain import Video
from app.services.extractors.youtube import YoutubeExtractor
from app.services.extractors.instagram import InstagramExtractor
from app.db.repositories.video_repository import VideoRepository
from app.services.pipeline.orchestrator import TranscriptEmbeddingPipeline
from app.core.errors import ExtractionError, InvalidUrlError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class VideoIngestionService:
    def __init__(self):
        self.youtube_extractor = YoutubeExtractor()
        self.instagram_extractor = InstagramExtractor()
        self.video_repo = VideoRepository()
        self.pipeline = TranscriptEmbeddingPipeline()

    def process_video(self, url: str, background_tasks: BackgroundTasks = None) -> Video:
        logger.info(f"Starting extraction for URL: {url}")
        try:
            if self.youtube_extractor.validate_url(url):
                logger.info("Detected YouTube URL")
                video = self.youtube_extractor.get_video_data(url)
            elif self.instagram_extractor.validate_url(url):
                logger.info("Detected Instagram URL")
                video = self.instagram_extractor.get_video_data(url)
            else:
                raise InvalidUrlError(url, "Unknown")
                
            logger.info(f"Saving video data to database for URL: {url}")
            
            existing = self.video_repo.get_video_by_url(url)
            if existing:
                logger.info(f"Video already exists in database, returning existing record: {url}")
                return existing
                
            saved_video = self.video_repo.insert_video(video)
            logger.info(f"Successfully processed and saved video: {url}")
            
            # Trigger embedding pipeline
            if background_tasks and saved_video.transcript:
                background_tasks.add_task(
                    self.pipeline.process_video_transcript, 
                    saved_video.id, 
                    saved_video.transcript, 
                    saved_video.platform
                )
                
            return saved_video
            
        except (ExtractionError, InvalidUrlError) as e:
            logger.error(f"Extraction failed for {url}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error processing {url}: {str(e)}")
            raise ExtractionError(f"Unexpected error: {str(e)}", "Unknown")

    def process_multiple_videos(self, youtube_url: str, instagram_url: str, background_tasks: BackgroundTasks = None) -> Tuple[Video, Video]:
        logger.info(f"Processing multiple videos: {youtube_url}, {instagram_url}")
        
        videoA = self.process_video(youtube_url, background_tasks)
        videoB = self.process_video(instagram_url, background_tasks)
        
        return videoA, videoB
