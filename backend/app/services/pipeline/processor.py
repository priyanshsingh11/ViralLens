import re
import unicodedata
import logging

logger = logging.getLogger(__name__)

class TranscriptProcessor:
    def clean_text(self, text: str) -> str:
        if not text:
            return ""
        
        text = self.normalize_unicode(text)
        text = self.remove_noise(text)
        text = self.remove_extra_whitespace(text)
        
        return text

    def normalize_unicode(self, text: str) -> str:
        return unicodedata.normalize("NFKC", text)

    def remove_noise(self, text: str) -> str:
        text = re.sub(r'\[.*?\]', '', text)
        text = re.sub(r'\(.*?\)', '', text)
        return text

    def remove_extra_whitespace(self, text: str) -> str:
        return re.sub(r'\s+', ' ', text).strip()
