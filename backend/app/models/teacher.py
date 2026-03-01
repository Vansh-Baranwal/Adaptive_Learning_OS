"""Teacher model."""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class Teacher(Base):
    """Teacher model."""
    
    __tablename__ = "teachers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    department = Column(String)
    
    # Relationships
    user = relationship("User", back_populates="teacher")
    assignments = relationship("Assignment", back_populates="teacher", cascade="all, delete-orphan")
