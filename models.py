from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class SessionHistory(BaseModel):
    customer_id: str
    session_id: str
    messages: List[ChatMessage] = Field(default_factory=list)
    
    def add_message(self, content: str) -> None:
        self.messages.append(ChatMessage(content=content))
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
