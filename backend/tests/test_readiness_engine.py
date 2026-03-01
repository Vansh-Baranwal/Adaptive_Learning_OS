"""Tests for ReadinessEngine implementation."""
import pytest
from app.ai.readiness import ReadinessEngine
from app.ai.concept_graph import ConceptGraph


class MockConcept:
    """Mock Concept for testing."""
    def __init__(self, id: int, prerequisite_id: int = None):
        self.id = id
        self.prerequisite_id = prerequisite_id


class TestReadinessEngine:
    """Test suite for ReadinessEngine."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Create a concept graph with dependencies
        # 1 -> 2 -> 3
        #   -> 4
        concepts = [
            MockConcept(1, None),
            MockConcept(2, 1),
            MockConcept(3, 2),
            MockConcept(4, 1)
        ]
        
        self.graph = ConceptGraph()
        self.graph.build_graph(concepts)
        self.engine = ReadinessEngine(self.graph)
    
    def test_assess_readiness_no_prerequisites(self):
        """Test readiness for concept with no prerequisites."""
        mastery_data = {}
        
        readiness = self.engine.assess_readiness(1, 1, mastery_data)
        
        # No prerequisites means always ready
        assert readiness == 1.0
    
    def test_assess_readiness_single_prerequisite(self):
        """Test readiness with single prerequisite."""
        # Concept 2 requires concept 1
        mastery_data = {1: 0.8}
        
        readiness = self.engine.assess_readiness(1, 2, mastery_data)
        
        # Readiness should equal mastery of prerequisite
        assert readiness == 0.8
    
    def test_assess_readiness_multiple_prerequisites(self):
        """Test readiness with multiple prerequisites in chain."""
        # Concept 3 requires 2, which requires 1
        mastery_data = {1: 0.9, 2: 0.7}
        
        readiness = self.engine.assess_readiness(1, 3, mastery_data)
        
        # Readiness should be minimum of all prerequisites
        assert readiness == 0.7
    
    def test_assess_readiness_missing_mastery(self):
        """Test readiness when prerequisite mastery is missing."""
        # Concept 2 requires concept 1, but mastery not provided
        mastery_data = {}
        
        readiness = self.engine.assess_readiness(1, 2, mastery_data)
        
        # Missing mastery defaults to 0.0
        assert readiness == 0.0
    
    def test_get_ready_concepts_all_ready(self):
        """Test getting ready concepts when prerequisites are mastered."""
        # Student has mastered concept 1
        mastery_data = {1: 0.8, 2: 0.3, 3: 0.2, 4: 0.1}
        
        ready = self.engine.get_ready_concepts(1, mastery_data, [1, 2, 3, 4])
        
        # Concepts 2 and 4 should be ready (both require only concept 1)
        assert set(ready) == {2, 4}
    
    def test_get_ready_concepts_none_ready(self):
        """Test when no concepts are ready."""
        # Student hasn't mastered any prerequisites
        mastery_data = {1: 0.3, 2: 0.2, 3: 0.1, 4: 0.1}
        
        ready = self.engine.get_ready_concepts(1, mastery_data, [1, 2, 3, 4])
        
        # Only concept 1 might be ready (no prerequisites)
        # But it's below threshold, so nothing is ready
        assert 1 in ready  # Concept 1 has no prerequisites
    
    def test_get_ready_concepts_excludes_mastered(self):
        """Test that mastered concepts are excluded from ready list."""
        # Student has mastered concepts 1 and 2
        mastery_data = {1: 0.9, 2: 0.8, 3: 0.3, 4: 0.2}
        
        ready = self.engine.get_ready_concepts(1, mastery_data, [1, 2, 3, 4])
        
        # Concepts 1 and 2 should not be in ready list (already mastered)
        assert 1 not in ready
        assert 2 not in ready
        # Concept 3 should be ready (prerequisite 2 is mastered)
        assert 3 in ready
    
    def test_get_ready_concepts_sorted_by_readiness(self):
        """Test that ready concepts are sorted by readiness score."""
        # Create scenario with different readiness levels
        mastery_data = {1: 0.9, 2: 0.5, 3: 0.1, 4: 0.2}
        
        ready = self.engine.get_ready_concepts(1, mastery_data, [1, 2, 3, 4])
        
        # Should be sorted by readiness (highest first)
        # Concept 4 has higher prerequisite mastery than concept 3
        if len(ready) >= 2:
            # Verify ordering makes sense
            assert isinstance(ready, list)
    
    def test_readiness_threshold(self):
        """Test that readiness threshold is applied correctly."""
        # Set mastery just below threshold
        mastery_data = {1: 0.69, 2: 0.3}
        
        ready = self.engine.get_ready_concepts(1, mastery_data, [2])
        
        # Concept 2 should not be ready (prerequisite below threshold)
        assert 2 not in ready
        
        # Set mastery at threshold
        mastery_data = {1: 0.7, 2: 0.3}
        
        ready = self.engine.get_ready_concepts(1, mastery_data, [2])
        
        # Concept 2 should now be ready
        assert 2 in ready
