from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ChunkingService:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", "?", "!", " ", ""]
        )

    def chunk_transcript(self, transcript: str, video_id: str, platform: str) -> List[Dict[str, Any]]:
        if not transcript:
            return []
            
        chunks = self.splitter.split_text(transcript)
        logger.info(f"Split transcript into {len(chunks)} chunks.")
        
        results = []
        for index, text in enumerate(chunks):
            metadata = self.create_chunk_metadata(video_id, index, platform)
            results.append({
                "chunk_index": index,
                "text": text,
                "metadata": metadata
            })
        return results

    def create_chunk_metadata(self, video_id: str, index: int, platform: str) -> Dict[str, Any]:
        return {
            "video_id": video_id,
            "chunk_index": index,
            "platform": platform
        }
