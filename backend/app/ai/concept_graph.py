"""Concept Graph - Manages concept dependency graph."""
from typing import List, Set, Dict, Optional
from collections import deque
from app.models.concept import Concept


class ConceptGraph:
    """Manages concept dependency graph."""
    
    def __init__(self):
        """Initialize the concept graph."""
        # graph[concept_id] = prerequisite_id (direct prerequisite)
        self.graph: Dict[int, Optional[int]] = {}
        # reverse_graph[concept_id] = [dependent_ids] (concepts that depend on this one)
        self.reverse_graph: Dict[int, List[int]] = {}
    
    def build_graph(self, concepts: List[Concept]) -> None:
        """
        Build dependency graph from concept list.
        
        Args:
            concepts: List of all concepts with prerequisites
        """
        self.graph = {}
        self.reverse_graph = {}
        
        # Build forward graph (concept -> prerequisite)
        for concept in concepts:
            self.graph[concept.id] = concept.prerequisite_id
            
            # Initialize reverse graph entry
            if concept.id not in self.reverse_graph:
                self.reverse_graph[concept.id] = []
        
        # Build reverse graph (prerequisite -> dependents)
        for concept in concepts:
            if concept.prerequisite_id is not None:
                if concept.prerequisite_id not in self.reverse_graph:
                    self.reverse_graph[concept.prerequisite_id] = []
                self.reverse_graph[concept.prerequisite_id].append(concept.id)
    
    def get_prerequisites(self, concept_id: int) -> List[int]:
        """
        Get all prerequisite concept IDs (transitive closure).
        
        This returns all prerequisites needed before learning the target concept,
        following the prerequisite chain recursively.
        
        Args:
            concept_id: Target concept ID
            
        Returns:
            List of prerequisite concept IDs (ordered from root to immediate prerequisite)
        """
        if concept_id not in self.graph:
            return []
        
        prerequisites = []
        current_id = concept_id
        visited = set()
        
        # Follow the prerequisite chain
        while current_id in self.graph and self.graph[current_id] is not None:
            prereq_id = self.graph[current_id]
            
            # Avoid cycles
            if prereq_id in visited:
                break
            
            visited.add(prereq_id)
            prerequisites.append(prereq_id)
            current_id = prereq_id
        
        # Reverse to get root-to-leaf order
        prerequisites.reverse()
        return prerequisites
    
    def get_dependents(self, concept_id: int) -> List[int]:
        """
        Get all concepts that depend on this concept (direct dependents only).
        
        Args:
            concept_id: Source concept ID
            
        Returns:
            List of dependent concept IDs
        """
        if concept_id not in self.reverse_graph:
            return []
        
        return self.reverse_graph[concept_id].copy()
    
    def get_learning_path(self, start_concept_id: int, end_concept_id: int) -> List[int]:
        """
        Generate optimal learning path between concepts using BFS.
        
        This finds the shortest path through the prerequisite graph from
        start_concept to end_concept.
        
        Args:
            start_concept_id: Starting concept
            end_concept_id: Target concept
            
        Returns:
            Ordered list of concept IDs forming learning path (including start and end)
        """
        if start_concept_id == end_concept_id:
            return [start_concept_id]
        
        # BFS to find shortest path
        queue = deque([(start_concept_id, [start_concept_id])])
        visited = {start_concept_id}
        
        while queue:
            current_id, path = queue.popleft()
            
            # Check direct dependents (concepts that have current as prerequisite)
            if current_id in self.reverse_graph:
                for dependent_id in self.reverse_graph[current_id]:
                    if dependent_id == end_concept_id:
                        return path + [dependent_id]
                    
                    if dependent_id not in visited:
                        visited.add(dependent_id)
                        queue.append((dependent_id, path + [dependent_id]))
        
        # No path found - return prerequisites of end_concept starting from start
        # This handles the case where we need to learn prerequisites first
        end_prerequisites = self.get_prerequisites(end_concept_id)
        
        if start_concept_id in end_prerequisites:
            # start is a prerequisite of end
            idx = end_prerequisites.index(start_concept_id)
            return end_prerequisites[idx:] + [end_concept_id]
        
        # No direct path - return empty list
        return []
