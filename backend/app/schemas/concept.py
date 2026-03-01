"""Concept Pydantic schemas."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ConceptBase(BaseModel):
    """Base concept schema."""
    name: str
    description: Optional[str] = None
    difficulty_level: int = 1


class ConceptCreate(ConceptBase):
    """Schema for creating a new concept."""
    prerequisite_id: Optional[int] = None


class ConceptResponse(ConceptBase):
    """Schema for concept response."""
    id: int
    prerequisite_id: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True
