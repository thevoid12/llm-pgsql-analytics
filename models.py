from datetime import datetime
from typing import List
from enum import Enum
from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    USER = "user"
    AGENT = "agent"


class ConfidenceLevel(str, Enum):
    VERY_CONFIDENT = "very_confident"
    LESS_CONFIDENT = "less_confident"
    NOT_CONFIDENT = "not_confident"


class InputClassification(BaseModel):
    type: str
    reasoning: str = ""


class ChatMessage(BaseModel):
    content: str
    role: MessageRole
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class TableIdentificationResponse(BaseModel):
    confidence: ConfidenceLevel
    tables: List[str] = Field(default_factory=list)


class ColumnEntityMapping(BaseModel):
    column: str
    entity_value: str = ""


class TableColumnResponse(BaseModel):
    table: str
    columns: List[ColumnEntityMapping] = Field(default_factory=list)


class EntityColumnDetectionResponse(BaseModel):
    tables: List[TableColumnResponse] = Field(default_factory=list)


class SessionHistory(BaseModel):
    customer_id: str
    session_id: str
    messages: List[ChatMessage] = Field(default_factory=list)
    
    def add_message(self, content: str, role: MessageRole) -> None:
        self.messages.append(ChatMessage(content=content, role=role))
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
