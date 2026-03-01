"""Assignment Service - Handles assignment CRUD and rubric evaluation."""
from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.assignment import Assignment
from app.schemas.assignment import AssignmentCreate
from app.ai.rubric_engine import RubricEngine
from app.services.mastery_service import MasteryService
from app.core.exceptions import ResourceNotFoundError


class AssignmentService:
    """
    Service for assignment management and rubric-based evaluation.
    
    Handles assignment CRUD and submission evaluation using RubricEngine.
    May call MasteryService if assignment completion affects mastery.
    """
    
    def __init__(self, db: Session, rubric_engine: RubricEngine, mastery_service: Optional[MasteryService] = None):
        """
        Initialize assignment service.
        
        Args:
            db: Database session
            rubric_engine: Rubric engine for evaluation
            mastery_service: Optional mastery service for mastery updates
        """
        self.db = db
        self.rubric_engine = rubric_engine
        self.mastery_service = mastery_service
    
    def create_assignment(self, assignment_data: AssignmentCreate, teacher_id: int = None) -> Assignment:
        """
        Create a new assignment.
        
        Args:
            assignment_data: Assignment creation data
            teacher_id: Override teacher_id (from current user)
            
        Returns:
            Created assignment
        """
        assignment = Assignment(
            title=assignment_data.title,
            description=assignment_data.description,
            rubric=assignment_data.rubric,
            due_date=assignment_data.due_date,
            concept_id=assignment_data.concept_id,
            teacher_id=assignment_data.teacher_id,
        )
        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)
        return assignment
    
    def get_assignment(self, assignment_id: int) -> Assignment:
        """
        Get assignment by ID.
        
        Args:
            assignment_id: Assignment ID
            
        Returns:
            Assignment record
        """
        assignment = self.db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if not assignment:
            raise ResourceNotFoundError(f"Assignment {assignment_id} not found")
        return assignment
    
    def list_assignments(self, concept_id: Optional[int] = None) -> List[Assignment]:
        """
        List assignments, optionally filtered by concept.
        
        Args:
            concept_id: Optional concept ID filter
            
        Returns:
            List of assignments
        """
        query = self.db.query(Assignment)
        if concept_id is not None:
            query = query.filter(Assignment.concept_id == concept_id)
        return query.order_by(Assignment.created_at.desc()).all()
    
    def update_assignment(self, assignment_id: int, assignment_data: AssignmentCreate) -> Assignment:
        """
        Update an assignment.
        
        Args:
            assignment_id: Assignment ID
            assignment_data: Updated assignment data
            
        Returns:
            Updated assignment
        """
        assignment = self.get_assignment(assignment_id)
        assignment.title = assignment_data.title
        assignment.description = assignment_data.description
        assignment.rubric = assignment_data.rubric
        assignment.due_date = assignment_data.due_date
        assignment.concept_id = assignment_data.concept_id
        self.db.commit()
        self.db.refresh(assignment)
        return assignment
    
    def delete_assignment(self, assignment_id: int) -> None:
        """
        Delete an assignment.
        
        Args:
            assignment_id: Assignment ID
        """
        assignment = self.get_assignment(assignment_id)
        self.db.delete(assignment)
        self.db.commit()
    
    def submit_assignment(self, assignment_id: int, student_id: int, content: str) -> dict:
        """
        Submit and evaluate an assignment using rubric engine.
        
        Args:
            assignment_id: Assignment ID
            student_id: Student ID
            content: Student's submission content
            
        Returns:
            Evaluation results with score and feedback
        """
        # Placeholder - full rubric evaluation to be implemented in Phase 3
        raise NotImplementedError("Assignment submission will be implemented in Phase 3")
