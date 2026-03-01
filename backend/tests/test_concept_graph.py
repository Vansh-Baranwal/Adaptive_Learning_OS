"""Tests for ConceptGraph implementation."""
import pytest
from app.ai.concept_graph import ConceptGraph


class MockConcept:
    """Mock Concept for testing."""
    def __init__(self, id: int, prerequisite_id: int = None):
        self.id = id
        self.prerequisite_id = prerequisite_id


class TestConceptGraph:
    """Test suite for ConceptGraph."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.graph = ConceptGraph()
    
    def test_build_graph_simple(self):
        """Test building a simple concept graph."""
        concepts = [
            MockConcept(1, None),
            MockConcept(2, 1),
            MockConcept(3, 2)
        ]
        
        self.graph.build_graph(concepts)
        
        assert 1 in self.graph.graph
        assert 2 in self.graph.graph
        assert 3 in self.graph.graph
        assert self.graph.graph[1] is None
        assert self.graph.graph[2] == 1
        assert self.graph.graph[3] == 2
    
    def test_get_prerequisites_chain(self):
        """Test getting prerequisites in a chain."""
        concepts = [
            MockConcept(1, None),
            MockConcept(2, 1),
            MockConcept(3, 2),
            MockConcept(4, 3)
        ]
        
        self.graph.build_graph(concepts)
        
        # Concept 4 requires 3, 2, 1 (in that order from root)
        prereqs = self.graph.get_prerequisites(4)
        assert prereqs == [1, 2, 3]
        
        # Concept 2 requires only 1
        prereqs = self.graph.get_prerequisites(2)
        assert prereqs == [1]
        
        # Concept 1 has no prerequisites
        prereqs = self.graph.get_prerequisites(1)
        assert prereqs == []
    
    def test_get_prerequisites_no_concept(self):
        """Test getting prerequisites for non-existent concept."""
        concepts = [MockConcept(1, None)]
        self.graph.build_graph(concepts)
        
        prereqs = self.graph.get_prerequisites(999)
        assert prereqs == []
    
    def test_get_dependents(self):
        """Test getting dependent concepts."""
        concepts = [
            MockConcept(1, None),
            MockConcept(2, 1),
            MockConcept(3, 1),
            MockConcept(4, 2)
        ]
        
        self.graph.build_graph(concepts)
        
        # Concept 1 has dependents 2 and 3
        dependents = self.graph.get_dependents(1)
        assert set(dependents) == {2, 3}
        
        # Concept 2 has dependent 4
        dependents = self.graph.get_dependents(2)
        assert dependents == [4]
        
        # Concept 4 has no dependents
        dependents = self.graph.get_dependents(4)
        assert dependents == []
    
    def test_get_learning_path_direct(self):
        """Test learning path in a direct chain."""
        concepts = [
            MockConcept(1, None),
            MockConcept(2, 1),
            MockConcept(3, 2)
        ]
        
        self.graph.build_graph(concepts)
        
        # Path from 1 to 3 should be [1, 2, 3]
        path = self.graph.get_learning_path(1, 3)
        assert path == [1, 2, 3]
        
        # Path from 1 to 2 should be [1, 2]
        path = self.graph.get_learning_path(1, 2)
        assert path == [1, 2]
    
    def test_get_learning_path_same_concept(self):
        """Test learning path when start equals end."""
        concepts = [MockConcept(1, None)]
        self.graph.build_graph(concepts)
        
        path = self.graph.get_learning_path(1, 1)
        assert path == [1]
    
    def test_build_graph_with_branches(self):
        """Test building graph with multiple branches."""
        concepts = [
            MockConcept(1, None),
            MockConcept(2, 1),
            MockConcept(3, 1),
            MockConcept(4, 2),
            MockConcept(5, 3)
        ]
        
        self.graph.build_graph(concepts)
        
        # Verify forward graph
        assert self.graph.graph[4] == 2
        assert self.graph.graph[5] == 3
        
        # Verify reverse graph
        assert set(self.graph.get_dependents(1)) == {2, 3}
        assert self.graph.get_dependents(2) == [4]
        assert self.graph.get_dependents(3) == [5]
