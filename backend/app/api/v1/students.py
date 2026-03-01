"""Student routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db, get_mastery_service, get_student_service
from app.services.mastery_service import MasteryService
from app.services.student_service import StudentService
from app.schemas.mastery import MasteryResponse
from app.schemas.attempt import AttemptResponse
from app.core.middleware import get_current_user, require_role
from app.models.user import User


router = APIRouter(prefix="/students", tags=["students"])


@router.get("/{student_id}/mastery", response_model=List[MasteryResponse])
async def get_student_mastery(
    student_id: int,
    current_user: User = Depends(require_role(["teacher", "student"])),
    db: Session = Depends(get_db)
):
    """
    Get mastery levels for a student across all concepts.
    
    Args:
        student_id: Student ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List of mastery records
    """
    # Students can only view their own mastery
    if current_user.role == "student":
        student_service = get_student_service(db)
        student = student_service.get_student_by_user_id(current_user.id)
        if not student or student.id != student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot access other students' mastery data"
            )
    
    mastery_service = get_mastery_service(db)
    mastery_records = mastery_service.get_all_student_mastery(student_id)
    return mastery_records


@router.get("/{student_id}/attempts", response_model=List[AttemptResponse])
async def get_student_attempts(
    student_id: int,
    current_user: User = Depends(require_role(["teacher", "student"])),
    db: Session = Depends(get_db)
):
    """
    Get all attempts for a student.
    
    Args:
        student_id: Student ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List of attempt records
    """
    # Students can only view their own attempts
    if current_user.role == "student":
        student_service = get_student_service(db)
        student = student_service.get_student_by_user_id(current_user.id)
        if not student or student.id != student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot access other students' attempts"
            )
    
    student_service = get_student_service(db)
    attempts = student_service.get_student_attempts(student_id)
    return attempts
