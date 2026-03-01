"""Attempt Pydantic schemas."""
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class AttemptBase(BaseModel):
    """Base attempt schema."""
    content: str


class AttemptCreate(AttemptBase):
    """Schema for creating a new attempt."""
    student_id: int
    assignment_id: int
    concept_id: int


class AttemptResponse(AttemptBase):
    """Schema for attempt response."""
    id: int
    student_id: int
    assignment_id: int
    concept_id: int
    score: Optional[float]
    evaluation: Optional[Dict[str, Any]]
    submitted_at: datetime
    
    class Config:
        from_attributes = True
