"""Mastery Service - Handles mastery tracking and BKT updates."""
from sqlalchemy.orm import Session
from typing import Optional, List, Dict
from app.models.mastery import Mastery
from app.models.concept import Concept
from app.ai.mastery_engine import MasteryEngine


class MasteryService:
    """Service for mastery tracking and Bayesian Knowledge Tracing."""
    
    def __init__(self, db: Session, mastery_engine: MasteryEngine):
        """
        Initialize mastery service.
        
        Args:
            db: Database session
            mastery_engine: Mastery engine for BKT calculations
        """
        self.db = db
        self.mastery_engine = mastery_engine
    
    def get_student_mastery(self, student_id: int, concept_id: int) -> Optional[Mastery]:
        """
        Get current mastery level for student-concept pair.
        
        Args:
            student_id: Student ID
            concept_id: Concept ID
            
        Returns:
            Mastery record or None if not found
        """
        return self.db.query(Mastery).filter(
            Mastery.student_id == student_id,
            Mastery.concept_id == concept_id
        ).first()
    
    def update_mastery(self, student_id: int, concept_id: int, attempt_data: Dict) -> Mastery:
        """
        Update mastery based on new attempt using BKT.
        
        This is called by AttemptService after a quiz attempt is submitted.
        
        Args:
            student_id: Student ID
            concept_id: Concept ID
            attempt_data: Attempt result data. Should contain:
                - 'correct': bool indicating if attempt was correct
                - 'score': optional float score
            
        Returns:
            Updated mastery record
        """
        # Get or create mastery record
        mastery = self.get_student_mastery(student_id, concept_id)
        
        if mastery is None:
            # Create new mastery record with default BKT parameters
            mastery = Mastery(
                student_id=student_id,
                concept_id=concept_id,
                p_l=0.5,  # Initial mastery probability
                p_t=0.1,  # Learning rate
                p_g=0.25,  # Guess probability
                p_s=0.1,  # Slip probability
                attempt_count=0
            )
            self.db.add(mastery)
        
        # Prepare attempt result for BKT engine
        bkt_attempt = {
            'correct': attempt_data.get('correct', False),
            'p_t': mastery.p_t,
            'p_g': mastery.p_g,
            'p_s': mastery.p_s
        }
        
        # Update mastery using BKT
        new_p_l = self.mastery_engine.update_mastery_belief(
            current_mastery=mastery.p_l,
            attempt_result=bkt_attempt
        )
        
        # Update mastery record
        mastery.p_l = new_p_l
        mastery.attempt_count += 1
        
        # Commit changes
        self.db.commit()
        self.db.refresh(mastery)
        
        return mastery
    
    def predict_mastery(self, student_id: int, concept_id: int) -> float:
        """
        Predict future mastery level.
        
        Args:
            student_id: Student ID
            concept_id: Concept ID
            
        Returns:
            Predicted mastery probability (0.0 to 1.0)
        """
        mastery = self.get_student_mastery(student_id, concept_id)
        
        if mastery is None:
            # No mastery record, return default
            return 0.5
        
        # Current mastery is the prediction
        return mastery.p_l
    
    def get_all_student_mastery(self, student_id: int) -> List[Mastery]:
        """
        Get all mastery records for a student.
        
        Args:
            student_id: Student ID
            
        Returns:
            List of mastery records
        """
        return (
            self.db.query(Mastery)
            .filter(Mastery.student_id == student_id)
            .all()
        )
    
    def get_weak_concepts(self, student_id: int, threshold: float = 0.5) -> List[Dict]:
        """
        Get concepts where student has low mastery.
        
        Identifies concepts that need attention based on mastery probability.
        Returns concepts sorted by mastery level (lowest first).
        
        Args:
            student_id: Student ID
            threshold: Mastery threshold below which concepts are considered weak (default 0.5)
            
        Returns:
            List of dicts containing weak concept data:
            - concept_id: int
            - concept_name: str
            - mastery_level: float (p_l value)
            - attempt_count: int
        """
        # Query mastery records below threshold
        weak_masteries = self.db.query(Mastery, Concept).join(
            Concept, Mastery.concept_id == Concept.id
        ).filter(
            Mastery.student_id == student_id,
            Mastery.p_l < threshold
        ).order_by(
            Mastery.p_l.asc()  # Lowest mastery first
        ).all()
        
        # Format results
        weak_concepts = []
        for mastery, concept in weak_masteries:
            weak_concepts.append({
                'concept_id': concept.id,
                'concept_name': concept.name,
                'mastery_level': mastery.p_l,
                'attempt_count': mastery.attempt_count
            })
        
        return weak_concepts
