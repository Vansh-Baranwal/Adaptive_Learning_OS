"""Mastery model with Bayesian Knowledge Tracing parameters."""
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base


class Mastery(Base):
    """Mastery model with BKT parameters."""
    
    __tablename__ = "mastery"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    
    # Bayesian Knowledge Tracing parameters
    p_l = Column(Float, default=0.5, nullable=False)  # Current mastery probability
    p_t = Column(Float, default=0.1, nullable=False)  # Learning rate (probability of learning)
    p_g = Column(Float, default=0.25, nullable=False)  # Guess probability
    p_s = Column(Float, default=0.1, nullable=False)  # Slip probability
    
    # Metadata
    attempt_count = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="mastery")
    concept = relationship("Concept", back_populates="mastery")
    
    # Unique constraint and indexes
    __table_args__ = (
        UniqueConstraint('student_id', 'concept_id', name='uq_student_concept'),
        Index('idx_student_concept_mastery', 'student_id', 'concept_id'),
    )
