"""Teacher Service."""
from sqlalchemy.orm import Session
from typing import List, Dict
from app.models.teacher import Teacher
from app.models.student import Student
from app.models.mastery import Mastery
from app.models.concept import Concept
from app.models.assignment import Assignment
from app.models.attempt import Attempt
from app.core.exceptions import ResourceNotFoundError


class TeacherService:
    """Service for teacher operations."""
    
    def __init__(self, db: Session):
        """
        Initialize teacher service.
        
        Args:
            db: Database session
        """
        self.db = db
    
    def get_teacher(self, teacher_id: int) -> Teacher:
        """
        Get teacher by ID.
        
        Args:
            teacher_id: Teacher ID
            
        Returns:
            Teacher record
        """
        teacher = self.db.query(Teacher).filter(Teacher.id == teacher_id).first()
        if not teacher:
            raise ResourceNotFoundError(f"Teacher {teacher_id} not found")
        return teacher
    
    def get_teacher_by_user_id(self, user_id: int) -> Teacher:
        """
        Get teacher by user ID.
        
        Args:
            user_id: User ID
            
        Returns:
            Teacher record
        """
        return self.db.query(Teacher).filter(Teacher.user_id == user_id).first()
    
    def get_analytics(self, teacher_id: int) -> dict:
        """
        Get aggregated analytics for teacher's students.
        
        Args:
            teacher_id: Teacher ID
            
        Returns:
            Aggregated analytics
        """
        # Get teacher's assignments
        assignments = (
            self.db.query(Assignment)
            .filter(Assignment.teacher_id == teacher_id)
            .all()
        )
        
        assignment_ids = [a.id for a in assignments]
        
        # Get all attempts on teacher's assignments
        attempts = (
            self.db.query(Attempt)
            .filter(Attempt.assignment_id.in_(assignment_ids))
            .all()
        ) if assignment_ids else []
        
        # Unique students
        student_ids = list(set(a.student_id for a in attempts))
        
        # Calculate analytics
        total_attempts = len(attempts)
        scored_attempts = [a for a in attempts if a.score is not None]
        avg_score = (
            sum(a.score for a in scored_attempts) / len(scored_attempts)
            if scored_attempts
            else 0
        )
        
        return {
            "teacher_id": teacher_id,
            "total_assignments": len(assignments),
            "total_attempts": total_attempts,
            "unique_students": len(student_ids),
            "average_score": round(avg_score, 4),
            "assignments": [
                {
                    "id": a.id,
                    "title": a.title,
                    "concept_id": a.concept_id,
                }
                for a in assignments
            ],
        }
    
    def get_all_students_weak_concepts(
        self, teacher_id: int, threshold: float = 0.5
    ) -> List[Dict]:
        """
        Get weak concepts across all students for a teacher.
        
        Args:
            teacher_id: Teacher ID
            threshold: Mastery threshold
            
        Returns:
            Aggregated weak concepts data
        """
        # Get teacher's assignment concept IDs
        assignments = (
            self.db.query(Assignment)
            .filter(Assignment.teacher_id == teacher_id)
            .all()
        )
        concept_ids = list(set(a.concept_id for a in assignments))
        
        if not concept_ids:
            return []
        
        # Get mastery records below threshold for those concepts
        weak_records = (
            self.db.query(Mastery, Concept, Student)
            .join(Concept, Mastery.concept_id == Concept.id)
            .join(Student, Mastery.student_id == Student.id)
            .filter(
                Mastery.concept_id.in_(concept_ids),
                Mastery.p_l < threshold,
            )
            .order_by(Mastery.p_l.asc())
            .all()
        )
        
        return [
            {
                "student_id": student.id,
                "student_name": f"{student.first_name} {student.last_name}",
                "concept_id": concept.id,
                "concept_name": concept.name,
                "mastery_level": round(mastery.p_l, 4),
                "attempt_count": mastery.attempt_count,
            }
            for mastery, concept, student in weak_records
        ]
