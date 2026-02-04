import os
import json
import redis
from typing import Optional
from dotenv import load_dotenv
from models import SessionHistory, ChatMessage, MessageRole

load_dotenv()


class RedisSessionManager:
    def __init__(self) -> None:
        self.redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=int(os.getenv("REDIS_DB", 0)),
            decode_responses=True,
        )
        self.customer_id = os.getenv("CUSTOMER_ID", "cust_01")
        self.session_id = os.getenv("SESSION_ID", "550e8400-e29b-41d4-a716-446655440000")
    
    def _get_redis_key(self) -> str:
        return f"{self.customer_id}_{self.session_id}"
    
    def save_message(self, content: str, role: MessageRole, sql_content: str = "") -> None:
        key = self._get_redis_key()
        session_history = self.get_session_history()
        
        if session_history is None:
            session_history = SessionHistory(
                customer_id=self.customer_id,
                session_id=self.session_id
            )
        
        session_history.add_message(content, role, sql_content)
        self.redis_client.set(key, session_history.model_dump_json())
    
    def get_session_history(self) -> Optional[SessionHistory]:
        key = self._get_redis_key()
        data = self.redis_client.get(key)
        
        if data is None:
            return None
        
        return SessionHistory.model_validate_json(data)
    
    def clear_session(self) -> None:
        key = self._get_redis_key()
        self.redis_client.delete(key)
    
    def get_user_messages(self, limit: int = None) -> list[str]:
        session_history = self.get_session_history()
        
        if session_history is None or not session_history.messages:
            return []
        
        user_messages = [msg.content for msg in session_history.messages if msg.role == MessageRole.USER]
        
        if limit:
            return user_messages[-limit:]
        return user_messages
    
    def get_conversation_history_with_sql(self, limit: int = None) -> list[dict]:
        session_history = self.get_session_history()
        
        if session_history is None or not session_history.messages:
            return []
        
        history = []
        message_number = 1
        for msg in session_history.messages:
            if msg.role == MessageRole.USER:
                entry = {
                    "number": message_number,
                    "role": msg.role.value,
                    "content": msg.content
                }
                history.append(entry)
                message_number += 1
            elif msg.role == MessageRole.AGENT and msg.sql_content:
                entry = {
                    "number": message_number,
                    "role": msg.role.value,
                    "sql_content": msg.sql_content
                }
                history.append(entry)
                message_number += 1
        
        if limit:
            return history[-limit:]
        return history
    
    def close(self) -> None:
        self.redis_client.close()
