"""User Pydantic schemas."""
from pydantic import BaseModel, EmailStr
from typing import Literal, Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    role: Literal["student", "teacher"]


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str
    first_name: str
    last_name: str
    department: Optional[str] = None  # For teachers only


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """JWT token response schema."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data."""
    user_id: int
    role: str
