"""Teacher Pydantic schemas."""
from pydantic import BaseModel
from typing import Optional


class TeacherBase(BaseModel):
    """Base teacher schema."""
    first_name: str
    last_name: str
    department: Optional[str] = None


class TeacherCreate(TeacherBase):
    """Schema for creating a new teacher."""
    pass


class TeacherResponse(TeacherBase):
    """Schema for teacher response."""
    id: int
    user_id: int
    
    class Config:
        from_attributes = True
