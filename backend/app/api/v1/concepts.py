"""Concept routes."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db, get_concept_service
from app.services.concept_service import ConceptService
from app.schemas.concept import ConceptCreate, ConceptResponse
from app.core.middleware import require_role
from app.models.user import User


router = APIRouter(prefix="/concepts", tags=["concepts"])


@router.post("/", response_model=ConceptResponse, status_code=status.HTTP_201_CREATED)
async def create_concept(
    concept: ConceptCreate,
    current_user: User = Depends(require_role(["teacher"])),
    db: Session = Depends(get_db)
):
    """
    Create a new concept with optional prerequisite.
    
    Args:
        concept: Concept data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Created concept
    """
    concept_service = get_concept_service(db)
    new_concept = concept_service.create_concept(concept)
    return new_concept


@router.get("/{concept_id}/prerequisites", response_model=List[ConceptResponse])
async def get_concept_prerequisites(
    concept_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all prerequisite concepts for a given concept.
    
    Args:
        concept_id: Concept ID
        db: Database session
        
    Returns:
        List of prerequisite concepts
    """
    concept_service = get_concept_service(db)
    prerequisites = concept_service.get_prerequisites(concept_id)
    return prerequisites


@router.get("/{concept_id}/dependents", response_model=List[ConceptResponse])
async def get_concept_dependents(
    concept_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all concepts that depend on this concept.
    
    Args:
        concept_id: Concept ID
        db: Database session
        
    Returns:
        List of dependent concepts
    """
    concept_service = get_concept_service(db)
    dependents = concept_service.get_dependents(concept_id)
    return dependents
