"""Mastery Pydantic schemas."""
from pydantic import BaseModel
from datetime import datetime


class MasteryBase(BaseModel):
    """Base mastery schema."""
    p_l: float  # Current mastery probability
    p_t: float  # Learning rate
    p_g: float  # Guess probability
    p_s: float  # Slip probability
    attempt_count: int


class MasteryResponse(MasteryBase):
    """Schema for mastery response."""
    id: int
    student_id: int
    concept_id: int
    last_updated: datetime
    
    class Config:
        from_attributes = True
