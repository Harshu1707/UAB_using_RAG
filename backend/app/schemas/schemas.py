from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: str = "student"

class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead

class ChatRequest(BaseModel):
    message: str
    conversation_id: int | None = None

class ChatResponse(BaseModel):
    answer: str
    intent: str
    sources: list[dict] = []

class StudentRead(BaseModel):
    StudentID: str
    Name: str
    Course: str
    Semester: int
    Marks: float
    Attendance: float
    CGPA: float
    Department: str
    model_config = {"from_attributes": True}

class WebSearchRequest(BaseModel):
    query: str
