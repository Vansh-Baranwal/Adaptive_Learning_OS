"""Concept Service."""
from sqlalchemy.orm import Session
from typing import List
from app.models.concept import Concept
from app.schemas.concept import ConceptCreate
from app.ai.concept_graph import ConceptGraph
from app.core.exceptions import ResourceNotFoundError


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
        concept = Concept(
            name=concept_data.name,
            description=concept_data.description,
            difficulty_level=concept_data.difficulty_level,
            prerequisite_id=concept_data.prerequisite_id,
        )
        self.db.add(concept)
        self.db.commit()
        self.db.refresh(concept)
        return concept
    
    def get_concept(self, concept_id: int) -> Concept:
        """
        Get concept by ID.
        
        Args:
            concept_id: Concept ID
            
        Returns:
            Concept record
        """
        concept = self.db.query(Concept).filter(Concept.id == concept_id).first()
        if not concept:
            raise ResourceNotFoundError(f"Concept {concept_id} not found")
        return concept
    
    def get_prerequisites(self, concept_id: int) -> List[Concept]:
        """
        Get all prerequisite concepts (walks the chain).
        
        Args:
            concept_id: Concept ID
            
        Returns:
            List of prerequisite concepts
        """
        concept = self.get_concept(concept_id)
        prerequisites = []
        current = concept
        while current.prerequisite_id is not None:
            prereq = self.db.query(Concept).filter(Concept.id == current.prerequisite_id).first()
            if prereq is None or prereq in prerequisites:
                break  # Prevent infinite loops
            prerequisites.append(prereq)
            current = prereq
        return prerequisites
    
    def get_dependents(self, concept_id: int) -> List[Concept]:
        """
        Get all concepts that depend on this concept.
        
        Args:
            concept_id: Concept ID
            
        Returns:
            List of dependent concepts
        """
        # Make sure concept exists
        self.get_concept(concept_id)
        return (
            self.db.query(Concept)
            .filter(Concept.prerequisite_id == concept_id)
            .all()
        )
    
    def get_learning_path(self, student_id: int, target_concept_id: int) -> List[Concept]:
        """
        Generate optimal learning path (calls AI module).
        
        Args:
            student_id: Student ID
            target_concept_id: Target concept ID
            
        Returns:
            Ordered list of concepts forming learning path
        """
        # Get prerequisites and return them in order
        prerequisites = self.get_prerequisites(target_concept_id)
        prerequisites.reverse()  # Start from the most fundamental
        target = self.get_concept(target_concept_id)
        prerequisites.append(target)
        return prerequisites
