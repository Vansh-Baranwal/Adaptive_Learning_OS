"""Assignment Pydantic schemas."""
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class AssignmentBase(BaseModel):
    """Base assignment schema."""
    title: str
    description: Optional[str] = None
    rubric: Optional[Dict[str, Any]] = None
    due_date: Optional[datetime] = None


class AssignmentCreate(AssignmentBase):
    """Schema for creating a new assignment."""
    concept_id: int
    teacher_id: int


class AssignmentResponse(AssignmentBase):
    """Schema for assignment response."""
    id: int
    concept_id: int
    teacher_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
