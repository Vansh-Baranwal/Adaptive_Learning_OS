"""Attempt model."""
from sqlalchemy import Column, Integer, Text, Float, DateTime, ForeignKey, JSON, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base


class Attempt(Base):
    """Attempt model for student submissions."""
    
    __tablename__ = "attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    content = Column(Text, nullable=False)
    score = Column(Float)
    evaluation = Column(JSON)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="attempts")
    assignment = relationship("Assignment", back_populates="attempts")
    concept = relationship("Concept", back_populates="attempts")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_student_assignment', 'student_id', 'assignment_id'),
        Index('idx_student_concept', 'student_id', 'concept_id'),
    )
