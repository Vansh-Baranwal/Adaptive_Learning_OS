"""Student Pydantic schemas."""
from pydantic import BaseModel
from datetime import datetime


class StudentBase(BaseModel):
    """Base student schema."""
    first_name: str
    last_name: str


class StudentCreate(StudentBase):
    """Schema for creating a new student."""
    pass


class StudentResponse(StudentBase):
    """Schema for student response."""
    id: int
    user_id: int
    enrolled_at: datetime
    
    class Config:
        from_attributes = True
