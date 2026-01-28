from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class UserQuestion(BaseModel):
    question: str
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class SessionHistory(BaseModel):
    customer_id: str
    session_id: str
    questions: List[UserQuestion] = Field(default_factory=list)
    
    def add_question(self, question: str) -> None:
        self.questions.append(UserQuestion(question=question))
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
