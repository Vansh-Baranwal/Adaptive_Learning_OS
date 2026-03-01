"""Attempt Service - Handles quiz-style attempts only."""
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.attempt import Attempt
from app.schemas.attempt import AttemptCreate
from app.services.mastery_service import MasteryService
from app.core.exceptions import ResourceNotFoundError
import random


class AttemptService:
    """
    Service for quiz-style attempts.
    
    Handles quiz submissions and triggers mastery updates via MasteryService.
    Does NOT use RubricEngine - that's for AssignmentService.
    """
    
    def __init__(self, db: Session, mastery_service: MasteryService):
        """
        Initialize attempt service.
        
        Args:
            db: Database session
            mastery_service: Mastery service for BKT updates
        """
        self.db = db
        self.mastery_service = mastery_service
    
    def submit_attempt(self, attempt_data: AttemptCreate, user_id: int = None) -> Attempt:
        """
        Submit and process a new quiz attempt.
        
        Flow:
        1. Save attempt to database
        2. Simple score evaluation
        3. Trigger mastery update via MasteryService
        4. Return attempt with evaluation
        
        Args:
            attempt_data: Attempt submission data
            user_id: Current user ID (for validation)
            
        Returns:
            Created attempt record
        """
        # Simple scoring: generate a score based on content length as a heuristic
        # In production, this would use AI/ML evaluation
        content_len = len(attempt_data.content.strip())
        score = min(1.0, max(0.1, content_len / 500.0))  # Scale: 0.1-1.0
        # Add some randomness to make it realistic
        score = round(min(1.0, max(0.0, score + random.uniform(-0.15, 0.15))), 4)
        
        evaluation = {
            "score": score,
            "feedback": "Good attempt!" if score >= 0.7 else "Keep practicing, you can improve!",
            "correct": score >= 0.5,
        }
        
        attempt = Attempt(
            student_id=attempt_data.student_id,
            assignment_id=attempt_data.assignment_id,
            concept_id=attempt_data.concept_id,
            content=attempt_data.content,
            score=score,
            evaluation=evaluation,
        )
        self.db.add(attempt)
        self.db.flush()
        
        # Update mastery via BKT
        try:
            self.mastery_service.update_mastery(
                student_id=attempt_data.student_id,
                concept_id=attempt_data.concept_id,
                attempt_data={"correct": score >= 0.5, "score": score},
            )
        except Exception:
            pass  # Don't fail attempt submission if mastery update fails
        
        self.db.commit()
        self.db.refresh(attempt)
        return attempt
    
    def get_attempt(self, attempt_id: int) -> Attempt:
        """
        Get attempt by ID.
        
        Args:
            attempt_id: Attempt ID
            
        Returns:
            Attempt record
        """
        attempt = self.db.query(Attempt).filter(Attempt.id == attempt_id).first()
        if not attempt:
            raise ResourceNotFoundError(f"Attempt {attempt_id} not found")
        return attempt
    
    def get_student_attempts(self, student_id: int, concept_id: int = None) -> List[Attempt]:
        """
        Get all attempts for a student, optionally filtered by concept.
        
        Args:
            student_id: Student ID
            concept_id: Optional concept ID filter
            
        Returns:
            List of attempts
        """
        query = self.db.query(Attempt).filter(Attempt.student_id == student_id)
        if concept_id is not None:
            query = query.filter(Attempt.concept_id == concept_id)
        return query.order_by(Attempt.submitted_at.desc()).all()
