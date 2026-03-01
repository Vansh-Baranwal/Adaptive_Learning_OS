"""Teacher routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict
from app.dependencies import get_db, get_teacher_service, get_mastery_service
from app.services.teacher_service import TeacherService
from app.services.mastery_service import MasteryService
from app.core.middleware import require_role
from app.models.user import User


router = APIRouter(prefix="/teachers", tags=["teachers"])


@router.get("/{teacher_id}/analytics")
async def get_teacher_analytics(
    teacher_id: int,
    current_user: User = Depends(require_role(["teacher"])),
    db: Session = Depends(get_db)
):
    """
    Get analytics for teacher's students.
    
    Args:
        teacher_id: Teacher ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Analytics data
    """
    teacher_service = get_teacher_service(db)
    analytics = teacher_service.get_analytics(teacher_id)
    return analytics


@router.get("/{teacher_id}/students/weak-concepts")
async def get_students_weak_concepts(
    teacher_id: int,
    threshold: float = 0.5,
    current_user: User = Depends(require_role(["teacher"])),
    db: Session = Depends(get_db)
):
    """
    Get weak concepts across all students for a teacher.
    
    Args:
        teacher_id: Teacher ID
        threshold: Mastery threshold
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Aggregated weak concepts data
    """
    teacher_service = get_teacher_service(db)
    weak_concepts = teacher_service.get_all_students_weak_concepts(teacher_id, threshold)
    return weak_concepts
