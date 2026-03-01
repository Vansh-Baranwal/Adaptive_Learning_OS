"""Student Service."""
from sqlalchemy.orm import Session
from typing import List
from app.models.student import Student
from app.models.attempt import Attempt
from app.core.exceptions import ResourceNotFoundError


class StudentService:
    """Service for student operations."""
    
    def __init__(self, db: Session):
        """
        Initialize student service.
        
        Args:
            db: Database session
        """
        self.db = db
    
    def get_student(self, student_id: int) -> Student:
        """
        Get student by ID.
        
        Args:
            student_id: Student ID
            
        Returns:
            Student record
        """
        student = self.db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise ResourceNotFoundError(f"Student {student_id} not found")
        return student
    
    def get_student_by_user_id(self, user_id: int) -> Student:
        """
        Get student by user ID.
        
        Args:
            user_id: User ID
            
        Returns:
            Student record
        """
        return self.db.query(Student).filter(Student.user_id == user_id).first()
    
    def get_student_attempts(self, student_id: int) -> List[Attempt]:
        """
        Get all attempts for a student.
        
        Args:
            student_id: Student ID
            
        Returns:
            List of attempt records
        """
        return (
            self.db.query(Attempt)
            .filter(Attempt.student_id == student_id)
            .order_by(Attempt.submitted_at.desc())
            .all()
        )
