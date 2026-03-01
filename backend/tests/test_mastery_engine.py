"""Tests for MasteryEngine BKT implementation."""
import pytest
from app.ai.mastery_engine import MasteryEngine


class TestMasteryEngine:
    """Test suite for MasteryEngine."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.engine = MasteryEngine()
    
    def test_update_mastery_belief_correct_answer(self):
        """Test BKT update with correct answer increases mastery."""
        current_mastery = 0.5
        attempt_result = {
            'correct': True,
            'p_t': 0.1,
            'p_g': 0.25,
            'p_s': 0.1
        }
        
        updated_mastery = self.engine.update_mastery_belief(current_mastery, attempt_result)
        
        # Correct answer should increase mastery
        assert updated_mastery > current_mastery
        assert 0.0 <= updated_mastery <= 1.0
    
    def test_update_mastery_belief_incorrect_answer(self):
        """Test BKT update with incorrect answer decreases mastery."""
        current_mastery = 0.5
        attempt_result = {
            'correct': False,
            'p_t': 0.1,
            'p_g': 0.25,
            'p_s': 0.1
        }
        
        updated_mastery = self.engine.update_mastery_belief(current_mastery, attempt_result)
        
        # Incorrect answer should decrease mastery
        assert updated_mastery < current_mastery
        assert 0.0 <= updated_mastery <= 1.0
    
    def test_update_mastery_belief_bounds(self):
        """Test that mastery stays within [0, 1] bounds."""
        # Test with very high mastery
        high_mastery = 0.99
        attempt_result = {
            'correct': True,
            'p_t': 0.5,
            'p_g': 0.25,
            'p_s': 0.1
        }
        
        updated = self.engine.update_mastery_belief(high_mastery, attempt_result)
        assert 0.0 <= updated <= 1.0
        
        # Test with very low mastery
        low_mastery = 0.01
        attempt_result['correct'] = False
        
        updated = self.engine.update_mastery_belief(low_mastery, attempt_result)
        assert 0.0 <= updated <= 1.0
    
    def test_predict_mastery_empty_history(self):
        """Test prediction with no history returns default."""
        mastery = self.engine.predict_mastery([], concept_id=1)
        assert mastery == 0.5
    
    def test_predict_mastery_with_history(self):
        """Test prediction applies BKT over history."""
        history = [
            {'correct': True, 'p_l': 0.5, 'p_t': 0.1, 'p_g': 0.25, 'p_s': 0.1},
            {'correct': True, 'p_l': 0.5, 'p_t': 0.1, 'p_g': 0.25, 'p_s': 0.1},
            {'correct': False, 'p_l': 0.5, 'p_t': 0.1, 'p_g': 0.25, 'p_s': 0.1}
        ]
        
        mastery = self.engine.predict_mastery(history, concept_id=1)
        
        # Should return a valid mastery level
        assert 0.0 <= mastery <= 1.0
        # With 2 correct and 1 incorrect, should be above initial
        assert mastery > 0.5
    
    def test_bkt_learning_effect(self):
        """Test that learning rate affects mastery updates."""
        current_mastery = 0.5
        
        # Low learning rate
        low_learning = {
            'correct': True,
            'p_t': 0.01,
            'p_g': 0.25,
            'p_s': 0.1
        }
        
        # High learning rate
        high_learning = {
            'correct': True,
            'p_t': 0.5,
            'p_g': 0.25,
            'p_s': 0.1
        }
        
        low_result = self.engine.update_mastery_belief(current_mastery, low_learning)
        high_result = self.engine.update_mastery_belief(current_mastery, high_learning)
        
        # Higher learning rate should result in larger mastery increase
        assert high_result > low_result
