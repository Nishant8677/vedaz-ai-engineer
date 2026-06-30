from pydantic import BaseModel, Field, field_validator
from typing import List, Literal, Optional

class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

    @field_validator("content")
    @classmethod
    def content_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Message content cannot be empty")
        return v

class Chat(BaseModel):
    messages: List[Message]
    
    @field_validator("messages")
    @classmethod
    def validate_messages(cls, v: List[Message]) -> List[Message]:
        if not v:
            raise ValueError("Chat must contain messages")
        if v[0].role != "system":
            raise ValueError("First message must have role 'system'")
        if v[-1].role != "assistant":
            raise ValueError("Last message must have role 'assistant'")
        
        # Check alternating roles
        # Note: sometimes a user might send multiple messages, but the assignment specifies alternating.
        for i in range(1, len(v)):
            if v[i].role == v[i-1].role:
                raise ValueError(f"Roles must alternate, found consecutive '{v[i].role}'")
            
        return v

class JudgeResponse(BaseModel):
    safety: int = Field(ge=1, le=5, description="Safety score from 1 to 5")
    warmth: int = Field(ge=1, le=5, description="Warmth score from 1 to 5")
    honesty: int = Field(ge=1, le=5, description="Honesty score from 1 to 5")
    astrology_limits: int = Field(ge=1, le=5, description="Astrology limits score from 1 to 5")
    consistency: int = Field(ge=1, le=5, description="Consistency score from 1 to 5")
    overall: float = Field(ge=1.0, le=5.0, description="Overall score")
    strengths: List[str] = Field(description="List of strengths")
    weaknesses: List[str] = Field(description="List of weaknesses")
    reasoning: str = Field(description="Explanation for the scores")

class SafetyEvaluation(BaseModel):
    is_safe: bool = Field(description="True if the conversation is safe, False otherwise")
    reason: str = Field(description="Explanation of why it is safe or unsafe")
