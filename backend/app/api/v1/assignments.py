"""Assignment routes."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db, get_assignment_service
from app.services.assignment_service import AssignmentService
from app.schemas.assignment import AssignmentCreate, AssignmentResponse
from app.core.middleware import require_role
from app.models.user import User


router = APIRouter(prefix="/assignments", tags=["assignments"])


@router.post("/", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED)
async def create_assignment(
    assignment: AssignmentCreate,
    current_user: User = Depends(require_role(["teacher"])),
    db: Session = Depends(get_db)
):
    """
    Create a new assignment.
    
    Args:
        assignment: Assignment data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Created assignment
    """
    assignment_service = get_assignment_service(db)
    new_assignment = assignment_service.create_assignment(assignment, current_user.id)
    return new_assignment


@router.get("/{assignment_id}", response_model=AssignmentResponse)
async def get_assignment(
    assignment_id: int,
    db: Session = Depends(get_db)
):
    """
    Get assignment details.
    
    Args:
        assignment_id: Assignment ID
        db: Database session
        
    Returns:
        Assignment details
    """
    assignment_service = get_assignment_service(db)
    assignment = assignment_service.get_assignment(assignment_id)
    return assignment


@router.get("/", response_model=List[AssignmentResponse])
async def list_assignments(
    concept_id: int = None,
    db: Session = Depends(get_db)
):
    """
    List all assignments, optionally filtered by concept.
    
    Args:
        concept_id: Optional concept ID filter
        db: Database session
        
    Returns:
        List of assignments
    """
    assignment_service = get_assignment_service(db)
    assignments = assignment_service.list_assignments(concept_id)
    return assignments


@router.put("/{assignment_id}", response_model=AssignmentResponse)
async def update_assignment(
    assignment_id: int,
    assignment: AssignmentCreate,
    current_user: User = Depends(require_role(["teacher"])),
    db: Session = Depends(get_db)
):
    """
    Update an assignment.
    
    Args:
        assignment_id: Assignment ID
        assignment: Updated assignment data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Updated assignment
    """
    assignment_service = get_assignment_service(db)
    updated_assignment = assignment_service.update_assignment(assignment_id, assignment)
    return updated_assignment


@router.delete("/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_assignment(
    assignment_id: int,
    current_user: User = Depends(require_role(["teacher"])),
    db: Session = Depends(get_db)
):
    """
    Delete an assignment.
    
    Args:
        assignment_id: Assignment ID
        current_user: Current authenticated user
        db: Database session
    """
    assignment_service = get_assignment_service(db)
    assignment_service.delete_assignment(assignment_id)
