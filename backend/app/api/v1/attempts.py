"""Attempt routes."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_attempt_service
from app.services.attempt_service import AttemptService
from app.schemas.attempt import AttemptCreate, AttemptResponse
from app.core.middleware import require_role
from app.models.user import User


router = APIRouter(prefix="/attempts", tags=["attempts"])


@router.post("/", response_model=AttemptResponse, status_code=status.HTTP_201_CREATED)
async def submit_attempt(
    attempt: AttemptCreate,
    current_user: User = Depends(require_role(["student"])),
    db: Session = Depends(get_db)
):
    """
    Submit a new attempt for an assignment.
    
    This triggers mastery updates via MasteryService.
    
    Args:
        attempt: Attempt data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Created attempt with evaluation
    """
    attempt_service = get_attempt_service(db)
    new_attempt = attempt_service.submit_attempt(attempt, current_user.id)
    return new_attempt


@router.get("/{attempt_id}", response_model=AttemptResponse)
async def get_attempt(
    attempt_id: int,
    current_user: User = Depends(require_role(["teacher", "student"])),
    db: Session = Depends(get_db)
):
    """
    Get attempt details.
    
    Args:
        attempt_id: Attempt ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Attempt details
    """
    attempt_service = get_attempt_service(db)
    attempt = attempt_service.get_attempt(attempt_id)
    return attempt
