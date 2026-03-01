"""Concept Service."""
from sqlalchemy.orm import Session
from typing import List
from app.models.concept import Concept
from app.schemas.concept import ConceptCreate
from app.ai.concept_graph import ConceptGraph


class ConceptService:
    """Service for concept operations and dependency management."""
    
    def __init__(self, db: Session, concept_graph: ConceptGraph):
        """
        Initialize concept service.
        
        Args:
            db: Database session
            concept_graph: Concept dependency graph
        """
        self.db = db
        self.concept_graph = concept_graph
    
    def create_concept(self, concept_data: ConceptCreate) -> Concept:
        """
        Create a new concept.
        
        Args:
            concept_data: Concept creation data
            
        Returns:
            Created concept
        """
        # Placeholder - will be implemented
        raise NotImplementedError("Concept creation will be implemented")
    
    def get_prerequisites(self, concept_id: int) -> List[Concept]:
        """
        Get all prerequisite concepts (calls AI module).
        
        Args:
            concept_id: Concept ID
            
        Returns:
            List of prerequisite concepts
        """
        # Placeholder - will be implemented in Phase 2
        raise NotImplementedError("Get prerequisites will be implemented in Phase 2")
    
    def get_learning_path(self, student_id: int, target_concept_id: int) -> List[Concept]:
        """
        Generate optimal learning path (calls AI module).
        
        Args:
            student_id: Student ID
            target_concept_id: Target concept ID
            
        Returns:
            Ordered list of concepts forming learning path
        """
        # Placeholder - will be implemented in Phase 2
        raise NotImplementedError("Learning path generation will be implemented in Phase 2")
