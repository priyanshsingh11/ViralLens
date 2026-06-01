from abc import ABC, abstractmethod
from typing import Dict, Any
from app.models.domain import Video

class BaseExtractor(ABC):
    @abstractmethod
    def validate_url(self, url: str) -> bool:
        """Validates if the provided URL is supported by this extractor."""
        pass

    @abstractmethod
    def extract_metadata(self, url: str) -> Dict[str, Any]:
        """Extracts metadata from the video URL."""
        pass

    @abstractmethod
    def get_video_data(self, url: str) -> Video:
        """Runs the complete extraction pipeline and returns a Video model."""
        pass
