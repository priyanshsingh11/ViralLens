class ExtractionError(Exception):
    """Raised when metadata or transcript extraction fails."""
    def __init__(self, message: str, platform: str):
        self.message = message
        self.platform = platform
        super().__init__(self.message)

class InvalidUrlError(Exception):
    """Raised when an invalid URL is provided."""
    def __init__(self, url: str, platform: str):
        self.message = f"Invalid {platform} URL provided: {url}"
        self.url = url
        self.platform = platform
        super().__init__(self.message)

class RateLimitError(Exception):
    """Raised when a platform rate limit is encountered."""
    def __init__(self, platform: str):
        self.message = f"Rate limit exceeded for {platform}. Please try again later."
        self.platform = platform
        super().__init__(self.message)
