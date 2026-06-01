from typing import List, Optional
from uuid import UUID
from app.db.repositories.base import BaseRepository
from app.models.domain import ChatSession, ChatMessage, Citation

class ChatRepository(BaseRepository):
    def create_session(self, session_name: Optional[str] = None) -> ChatSession:
        data = {}
        if session_name:
            data["session_name"] = session_name
        response = self.client.table("chat_sessions").insert(data).execute()
        return ChatSession(**response.data[0])

    def get_session(self, session_id: str | UUID) -> Optional[ChatSession]:
        response = self.client.table("chat_sessions").select("*").eq("id", str(session_id)).execute()
        if response.data:
            return ChatSession(**response.data[0])
        return None

    def insert_message(self, message: ChatMessage) -> ChatMessage:
        data = message.model_dump(exclude_none=True)
        if "id" in data and isinstance(data["id"], UUID):
            data["id"] = str(data["id"])
        data["session_id"] = str(data["session_id"])
        
        response = self.client.table("chat_messages").insert(data).execute()
        return ChatMessage(**response.data[0])

    def insert_citation(self, citation: Citation) -> Citation:
        data = citation.model_dump(exclude_none=True)
        if "id" in data and isinstance(data["id"], UUID):
            data["id"] = str(data["id"])
        data["message_id"] = str(data["message_id"])
        data["video_id"] = str(data["video_id"])
        data["chunk_id"] = str(data["chunk_id"])
        
        response = self.client.table("citations").insert(data).execute()
        return Citation(**response.data[0])
