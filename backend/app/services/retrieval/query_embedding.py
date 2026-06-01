import logging
from typing import List
from openai import OpenAI
from tenacity import retry, wait_exponential, stop_after_attempt
from app.core.config import settings

logger = logging.getLogger(__name__)

class QueryEmbeddingService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "text-embedding-3-small"

    @retry(wait=wait_exponential(multiplier=1, min=1, max=5), stop=stop_after_attempt(3))
    def embed_query(self, question: str) -> List[float]:
        logger.info(f"Generating embedding for query: '{question}'")
        response = self.client.embeddings.create(
            input=question,
            model=self.model
        )
        return response.data[0].embedding
