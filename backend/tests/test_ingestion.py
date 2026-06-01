import pytest
from app.services.extractors.youtube import YoutubeExtractor
from app.services.extractors.instagram import InstagramExtractor
from app.core.errors import InvalidUrlError

def test_youtube_url_validation():
    extractor = YoutubeExtractor()
    assert extractor.validate_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == True
    assert extractor.validate_url("https://youtu.be/dQw4w9WgXcQ") == True
    assert extractor.validate_url("https://www.instagram.com/reel/C3zY/") == False

def test_youtube_shorts_validation():
    extractor = YoutubeExtractor()
    assert extractor.validate_url("https://www.youtube.com/shorts/abcdefghijk") == True

def test_instagram_url_validation():
    extractor = InstagramExtractor()
    assert extractor.validate_url("https://www.instagram.com/reel/C3zY/") == True
    assert extractor.validate_url("https://www.instagram.com/p/C3zY/") == True
    assert extractor.validate_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == False

def test_youtube_invalid_url_extraction():
    extractor = YoutubeExtractor()
    with pytest.raises(InvalidUrlError):
        extractor.get_video_data("https://invalid.url.com")
        
def test_instagram_invalid_url_extraction():
    extractor = InstagramExtractor()
    with pytest.raises(InvalidUrlError):
        extractor.get_video_data("https://invalid.url.com")
