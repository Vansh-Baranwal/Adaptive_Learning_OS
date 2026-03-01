"""Student Service."""
from sqlalchemy.orm import Session
from app.models.student import Student


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
        # Placeholder - will be implemented
        raise NotImplementedError("Get student will be implemented")
    
    def get_student_by_user_id(self, user_id: int) -> Student:
        """
        Get student by user ID.
        
        Args:
            user_id: User ID
            
        Returns:
            Student record
        """
        # Placeholder - will be implemented
        raise NotImplementedError("Get student by user ID will be implemented")
