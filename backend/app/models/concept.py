"""Concept model."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base


class Concept(Base):
    """Concept model with prerequisite relationships."""
    
    __tablename__ = "concepts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text)
    prerequisite_id = Column(Integer, ForeignKey("concepts.id"), nullable=True)
    difficulty_level = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Self-referential relationship for prerequisites
    prerequisite = relationship("Concept", remote_side=[id], backref="dependents")
    
    # Other relationships
    assignments = relationship("Assignment", back_populates="concept", cascade="all, delete-orphan")
    mastery = relationship("Mastery", back_populates="concept", cascade="all, delete-orphan")
    attempts = relationship("Attempt", back_populates="concept", cascade="all, delete-orphan")
