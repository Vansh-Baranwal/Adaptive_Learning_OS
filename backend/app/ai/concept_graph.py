"""Concept Graph - Manages concept dependency graph."""
from typing import List
from app.models.concept import Concept


class ConceptGraph:
    """Manages concept dependency graph."""
    
    def __init__(self):
        """Initialize the concept graph."""
        self.graph = {}
    
    def build_graph(self, concepts: List[Concept]) -> None:
        """
        Build dependency graph from concept list.
        
        Args:
            concepts: List of all concepts with prerequisites
        """
        # Placeholder - will be implemented in Phase 2
        raise NotImplementedError("Graph building will be implemented in Phase 2")
    
    def get_prerequisites(self, concept_id: int) -> List[int]:
        """
        Get all prerequisite concept IDs (transitive closure).
        
        Args:
            concept_id: Target concept ID
            
        Returns:
            List of prerequisite concept IDs
        """
        # Placeholder - will be implemented in Phase 2
        raise NotImplementedError("Prerequisite resolution will be implemented in Phase 2")
    
    def get_dependents(self, concept_id: int) -> List[int]:
        """
        Get all concepts that depend on this concept.
        
        Args:
            concept_id: Source concept ID
            
        Returns:
            List of dependent concept IDs
        """
        # Placeholder - will be implemented in Phase 2
        raise NotImplementedError("Dependent resolution will be implemented in Phase 2")
    
    def get_learning_path(self, start_concept_id: int, end_concept_id: int) -> List[int]:
        """
        Generate optimal learning path between concepts.
        
        Args:
            start_concept_id: Starting concept
            end_concept_id: Target concept
            
        Returns:
            Ordered list of concept IDs forming learning path
        """
        # Placeholder - will be implemented in Phase 2
        raise NotImplementedError("Learning path generation will be implemented in Phase 2")
