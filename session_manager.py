import os
import json
import redis
from typing import Optional
from dotenv import load_dotenv
from models import SessionHistory, UserQuestion

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
    
    def save_question(self, question: str) -> None:
        key = self._get_redis_key()
        session_history = self.get_session_history()
        
        if session_history is None:
            session_history = SessionHistory(
                customer_id=self.customer_id,
                session_id=self.session_id
            )
        
        session_history.add_question(question)
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
    
    def close(self) -> None:
        self.redis_client.close()
