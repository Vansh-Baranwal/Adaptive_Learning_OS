"""Tests for MasteryService implementation."""
import pytest
from unittest.mock import Mock, MagicMock, patch
from app.services.mastery_service import MasteryService
from app.ai.mastery_engine import MasteryEngine
from app.models.mastery import Mastery
from app.models.concept import Concept


class TestMasteryService:
    """Test suite for MasteryService."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.db = Mock()
        self.engine = MasteryEngine()
        self.service = MasteryService(self.db, self.engine)
    
    def test_get_student_mastery_exists(self):
        """Test getting existing mastery record."""
        # Mock database query
        mock_mastery = Mock(spec=Mastery)
        mock_mastery.student_id = 1
        mock_mastery.concept_id = 1
        mock_mastery.p_l = 0.7
        
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = mock_mastery
        self.db.query.return_value = mock_query
        
        result = self.service.get_student_mastery(1, 1)
        
        assert result == mock_mastery
        self.db.query.assert_called_once_with(Mastery)
    
    def test_get_student_mastery_not_exists(self):
        """Test getting non-existent mastery record."""
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = None
        self.db.query.return_value = mock_query
        
        result = self.service.get_student_mastery(1, 999)
        
        assert result is None
    
    def test_update_mastery_new_record(self):
        """Test updating mastery creates new record if none exists."""
        # Mock no existing mastery
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = None
        
        # Create a mock mastery that will be created
        mock_new_mastery = Mock(spec=Mastery)
        mock_new_mastery.p_l = 0.5
        mock_new_mastery.p_t = 0.1
        mock_new_mastery.p_g = 0.25
        mock_new_mastery.p_s = 0.1
        mock_new_mastery.attempt_count = 0
        
        # Mock the refresh to return our mock
        self.db.refresh.return_value = None
        
        self.db.query.return_value = mock_query
        
        attempt_data = {'correct': True}
        
        # Patch Mastery constructor
        with patch('app.services.mastery_service.Mastery', return_value=mock_new_mastery):
            result = self.service.update_mastery(1, 1, attempt_data)
        
        # Should add new mastery record
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
    
    def test_update_mastery_existing_record(self):
        """Test updating existing mastery record."""
        # Mock existing mastery
        mock_mastery = Mock(spec=Mastery)
        mock_mastery.p_l = 0.5
        mock_mastery.p_t = 0.1
        mock_mastery.p_g = 0.25
        mock_mastery.p_s = 0.1
        mock_mastery.attempt_count = 5
        
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = mock_mastery
        self.db.query.return_value = mock_query
        
        attempt_data = {'correct': True}
        
        result = self.service.update_mastery(1, 1, attempt_data)
        
        # Should update mastery
        assert mock_mastery.p_l != 0.5  # Should be updated
        assert mock_mastery.attempt_count == 6
        self.db.commit.assert_called_once()
    
    def test_predict_mastery_exists(self):
        """Test predicting mastery when record exists."""
        mock_mastery = Mock(spec=Mastery)
        mock_mastery.p_l = 0.75
        
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = mock_mastery
        self.db.query.return_value = mock_query
        
        prediction = self.service.predict_mastery(1, 1)
        
        assert prediction == 0.75
    
    def test_predict_mastery_not_exists(self):
        """Test predicting mastery when no record exists."""
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = None
        self.db.query.return_value = mock_query
        
        prediction = self.service.predict_mastery(1, 999)
        
        # Should return default
        assert prediction == 0.5
    
    def test_get_weak_concepts(self):
        """Test getting weak concepts below threshold."""
        # Mock mastery and concept data
        mock_mastery1 = Mock(spec=Mastery)
        mock_mastery1.concept_id = 1
        mock_mastery1.p_l = 0.3
        mock_mastery1.attempt_count = 5
        
        mock_concept1 = Mock(spec=Concept)
        mock_concept1.id = 1
        mock_concept1.name = "Concept 1"
        
        mock_mastery2 = Mock(spec=Mastery)
        mock_mastery2.concept_id = 2
        mock_mastery2.p_l = 0.4
        mock_mastery2.attempt_count = 3
        
        mock_concept2 = Mock(spec=Concept)
        mock_concept2.id = 2
        mock_concept2.name = "Concept 2"
        
        # Mock query chain
        mock_query = Mock()
        mock_query.join.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.all.return_value = [
            (mock_mastery1, mock_concept1),
            (mock_mastery2, mock_concept2)
        ]
        self.db.query.return_value = mock_query
        
        weak_concepts = self.service.get_weak_concepts(1, threshold=0.5)
        
        assert len(weak_concepts) == 2
        assert weak_concepts[0]['concept_id'] == 1
        assert weak_concepts[0]['concept_name'] == "Concept 1"
        assert weak_concepts[0]['mastery_level'] == 0.3
        assert weak_concepts[1]['concept_id'] == 2
    
    def test_get_weak_concepts_empty(self):
        """Test getting weak concepts when none exist."""
        mock_query = Mock()
        mock_query.join.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.all.return_value = []
        self.db.query.return_value = mock_query
        
        weak_concepts = self.service.get_weak_concepts(1)
        
        assert weak_concepts == []
    
    def test_get_weak_concepts_custom_threshold(self):
        """Test getting weak concepts with custom threshold."""
        mock_query = Mock()
        mock_query.join.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.all.return_value = []
        self.db.query.return_value = mock_query
        
        weak_concepts = self.service.get_weak_concepts(1, threshold=0.7)
        
        # Verify filter was called (threshold should be used in query)
        assert mock_query.filter.called
