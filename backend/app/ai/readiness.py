"""Readiness Engine - Student readiness assessment."""
from typing import List, Dict
from app.ai.concept_graph import ConceptGraph


class ReadinessEngine:
    """Assesses student readiness for concepts."""
    
    def __init__(self, concept_graph: ConceptGraph):
        """
        Initialize the readiness engine.
        
        Args:
            concept_graph: Concept dependency graph
        """
        self.concept_graph = concept_graph
        self.readiness_threshold = 0.7  # Minimum mastery level for prerequisites
    
    def assess_readiness(self, student_id: int, concept_id: int, mastery_data: Dict[int, float]) -> float:
        """
        Assess if student is ready for a concept.
        
        Readiness is calculated based on the student's mastery of all prerequisite concepts.
        A student is considered ready if they have sufficient mastery of all prerequisites.
        
        Algorithm:
        1. Get all prerequisites for the target concept
        2. Check mastery level for each prerequisite
        3. Calculate readiness as the minimum mastery among prerequisites
        4. If no prerequisites, readiness is 1.0 (always ready)
        
        Args:
            student_id: Student ID
            concept_id: Target concept ID
            mastery_data: Dict mapping concept_id to mastery level (0.0 to 1.0)
            
        Returns:
            Readiness score (0.0 to 1.0)
        """
        # Get all prerequisites for this concept
        prerequisites = self.concept_graph.get_prerequisites(concept_id)
        
        # If no prerequisites, student is ready
        if not prerequisites:
            return 1.0
        
        # Calculate readiness based on prerequisite mastery
        # Use minimum mastery among prerequisites as the readiness score
        prerequisite_masteries = []
        
        for prereq_id in prerequisites:
            mastery = mastery_data.get(prereq_id, 0.0)
            prerequisite_masteries.append(mastery)
        
        # Readiness is the minimum mastery among all prerequisites
        # This ensures all prerequisites are sufficiently mastered
        if prerequisite_masteries:
            readiness = min(prerequisite_masteries)
        else:
            readiness = 1.0
        
        return readiness
    
    def get_ready_concepts(self, student_id: int, mastery_data: Dict[int, float], 
                          all_concept_ids: List[int] = None) -> List[int]:
        """
        Get list of concepts student is ready to learn.
        
        A concept is considered "ready" if:
        1. The student hasn't mastered it yet (mastery < threshold)
        2. All prerequisites are sufficiently mastered (readiness >= threshold)
        
        Args:
            student_id: Student ID
            mastery_data: Dict mapping concept_id to mastery level (0.0 to 1.0)
            all_concept_ids: Optional list of all concept IDs to check. If None,
                           checks all concepts in mastery_data
            
        Returns:
            List of concept IDs student is ready for, sorted by readiness (highest first)
        """
        if all_concept_ids is None:
            # Check all concepts in the graph
            all_concept_ids = list(self.concept_graph.graph.keys())
        
        ready_concepts = []
        
        for concept_id in all_concept_ids:
            # Get current mastery for this concept
            current_mastery = mastery_data.get(concept_id, 0.0)
            
            # Skip if already mastered
            if current_mastery >= self.readiness_threshold:
                continue
            
            # Assess readiness for this concept
            readiness = self.assess_readiness(student_id, concept_id, mastery_data)
            
            # If ready (prerequisites mastered), add to list
            if readiness >= self.readiness_threshold:
                ready_concepts.append((concept_id, readiness))
        
        # Sort by readiness score (highest first)
        ready_concepts.sort(key=lambda x: x[1], reverse=True)
        
        # Return just the concept IDs
        return [concept_id for concept_id, _ in ready_concepts]
