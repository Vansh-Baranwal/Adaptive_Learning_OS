"""Mastery tracking routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict
from app.dependencies import get_db, get_mastery_service
from app.services.mastery_service import MasteryService
from app.schemas.mastery import MasteryResponse
from app.core.middleware import require_role
from app.models.user import User


router = APIRouter(prefix="/mastery", tags=["mastery"])


@router.get("/student/{student_id}/concept/{concept_id}", response_model=MasteryResponse)
async def get_mastery(
    student_id: int,
    concept_id: int,
    current_user: User = Depends(require_role(["teacher", "student"])),
    db: Session = Depends(get_db)
):
    """
    Get mastery level for a specific student-concept pair.
    
    Args:
        student_id: Student ID
        concept_id: Concept ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Mastery record
    """
    mastery_service = get_mastery_service(db)
    mastery = mastery_service.get_student_mastery(student_id, concept_id)
    return mastery


@router.get("/student/{student_id}/weak-concepts")
async def get_weak_concepts(
    student_id: int,
    threshold: float = 0.5,
    current_user: User = Depends(require_role(["teacher", "student"])),
    db: Session = Depends(get_db)
):
    """
    Get concepts where student has low mastery.
    
    Args:
        student_id: Student ID
        threshold: Mastery threshold (default 0.5)
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List of weak concepts with mastery data
    """
    mastery_service = get_mastery_service(db)
    weak_concepts = mastery_service.get_weak_concepts(student_id, threshold)
    return weak_concepts


@router.get("/student/{student_id}/predict/{concept_id}")
async def predict_mastery(
    student_id: int,
    concept_id: int,
    current_user: User = Depends(require_role(["teacher", "student"])),
    db: Session = Depends(get_db)
):
    """
    Predict future mastery level for a student-concept pair.
    
    Args:
        student_id: Student ID
        concept_id: Concept ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Predicted mastery probability
    """
    mastery_service = get_mastery_service(db)
    prediction = mastery_service.predict_mastery(student_id, concept_id)
    return {"student_id": student_id, "concept_id": concept_id, "predicted_mastery": prediction}
