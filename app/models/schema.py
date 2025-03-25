from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
import enum

class Role(str, enum.Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class Message(BaseModel):
    role: Role
    content: str = Field(..., description="Content of the message")

class PatientInfo(BaseModel):
    age: Optional[int] = Field(None, description="Patient age in years")
    gender: Optional[str] = Field(None, description="Patient gender")
    medical_history: Optional[List[str]] = Field(None, description="List of relevant medical history items")
    current_medications: Optional[List[str]] = Field(None, description="List of current medications")
    symptoms: Optional[List[str]] = Field(None, description="List of current symptoms")
    vitals: Optional[Dict[str, Any]] = Field(None, description="Vital measurements")

class MedicalQueryRequest(BaseModel):
    patient_info: PatientInfo = Field(..., description="Patient information")
    query: str = Field(..., description="Medical query or question")
    additional_context: Optional[str] = Field(None, description="Any additional context for the query")
    conversation_history: Optional[List[Message]] = Field(default_factory=list, description="Previous conversation history")
    model: Optional[str] = Field(None, description="OpenAI model to use")

class FeedbackType(str, enum.Enum):
    HELPFUL = "helpful"
    INCORRECT = "incorrect"
    HARMFUL = "harmful"
    IRRELEVANT = "irrelevant"
    OTHER = "other"

class MedicalQueryResponse(BaseModel):
    response_id: str = Field(..., description="Unique ID for this response")
    response: str = Field(..., description="Generated medical response")
    disclaimer: str = Field(..., description="Medical and AI usage disclaimer")
    model_used: str = Field(..., description="AI model used for generation")
    created_at: datetime = Field(..., description="Timestamp of response creation")
    tokens_used: Optional[int] = Field(None, description="Total tokens used")

class FeedbackRequest(BaseModel):
    response_id: str = Field(..., description="ID of the response being rated")
    feedback_type: FeedbackType = Field(..., description="Type of feedback")
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating from 1-5")
    comment: Optional[str] = Field(None, description="Additional feedback comments")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str