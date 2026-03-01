"""Tests for RubricEngine implementation."""
import pytest
from app.ai.rubric_engine import RubricEngine


class TestRubricEngine:
    """Test suite for RubricEngine."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.engine = RubricEngine()
    
    def test_evaluate_with_keywords(self):
        """Test evaluation with keyword matching."""
        rubric = {
            "criteria": [
                {
                    "name": "Understanding of calculus",
                    "max_points": 50,
                    "keywords": ["derivative", "integral", "limit"],
                    "min_length": 100
                }
            ],
            "total_points": 100
        }
        
        content = "The derivative of a function measures the rate of change. " \
                 "The integral represents the area under a curve. " \
                 "A limit describes the behavior of a function as it approaches a point."
        
        result = self.engine.evaluate(content, rubric)
        
        assert "total_score" in result
        assert "max_score" in result
        assert "percentage" in result
        assert result["total_score"] > 0
        assert result["max_score"] == 50
    
    def test_evaluate_missing_keywords(self):
        """Test evaluation when keywords are missing."""
        rubric = {
            "criteria": [
                {
                    "name": "Key concepts",
                    "max_points": 100,
                    "keywords": ["quantum", "mechanics", "wave"],
                    "min_length": 50
                }
            ]
        }
        
        content = "This is a short answer about something else entirely."
        
        result = self.engine.evaluate(content, rubric)
        
        # Should have lower score due to missing keywords
        assert result["total_score"] < result["max_score"]
    
    def test_evaluate_length_requirement(self):
        """Test evaluation with length requirement."""
        rubric = {
            "criteria": [
                {
                    "name": "Detailed explanation",
                    "max_points": 100,
                    "min_length": 200
                }
            ]
        }
        
        short_content = "Too short."
        long_content = "A" * 250
        
        short_result = self.engine.evaluate(short_content, rubric)
        long_result = self.engine.evaluate(long_content, rubric)
        
        # Longer content should score higher
        assert long_result["total_score"] > short_result["total_score"]
    
    def test_evaluate_multiple_criteria(self):
        """Test evaluation with multiple criteria."""
        rubric = {
            "criteria": [
                {
                    "name": "Criterion 1",
                    "max_points": 50,
                    "keywords": ["test1"]
                },
                {
                    "name": "Criterion 2",
                    "max_points": 50,
                    "keywords": ["test2"]
                }
            ],
            "total_points": 100
        }
        
        content = "This content includes test1 and test2 keywords."
        
        result = self.engine.evaluate(content, rubric)
        
        assert len(result["criteria_scores"]) == 2
        assert result["max_score"] == 100
    
    def test_evaluate_no_rubric(self):
        """Test evaluation with no rubric."""
        result = self.engine.evaluate("Some content", {})
        
        assert result["total_score"] == 0.0
        assert result["criteria_scores"] == []
    
    def test_evaluate_empty_criteria(self):
        """Test evaluation with empty criteria list."""
        rubric = {"criteria": [], "total_points": 100}
        
        result = self.engine.evaluate("Some content", rubric)
        
        assert result["total_score"] == 0.0
        assert result["criteria_scores"] == []
    
    def test_generate_feedback_excellent(self):
        """Test feedback generation for excellent score."""
        evaluation = {
            "total_score": 95,
            "max_score": 100,
            "percentage": 95.0,
            "criteria_scores": [
                {
                    "criterion": "Understanding",
                    "score": 95,
                    "max_score": 100,
                    "feedback": "Great work"
                }
            ]
        }
        
        feedback = self.engine.generate_feedback(evaluation)
        
        assert "95.0/100.0" in feedback
        assert "95.0%" in feedback
        assert "Excellent" in feedback
    
    def test_generate_feedback_needs_improvement(self):
        """Test feedback generation for low score."""
        evaluation = {
            "total_score": 50,
            "max_score": 100,
            "percentage": 50.0,
            "criteria_scores": []
        }
        
        feedback = self.engine.generate_feedback(evaluation)
        
        assert "50.0/100.0" in feedback
        assert "improvement" in feedback.lower()
    
    def test_generate_feedback_empty(self):
        """Test feedback generation with empty evaluation."""
        feedback = self.engine.generate_feedback({})
        
        assert "No evaluation data" in feedback
    
    def test_generate_feedback_with_criteria(self):
        """Test feedback includes criterion details."""
        evaluation = {
            "total_score": 75,
            "max_score": 100,
            "percentage": 75.0,
            "criteria_scores": [
                {
                    "criterion": "Criterion A",
                    "score": 40,
                    "max_score": 50,
                    "feedback": "Good understanding"
                },
                {
                    "criterion": "Criterion B",
                    "score": 35,
                    "max_score": 50,
                    "feedback": "Needs more detail"
                }
            ]
        }
        
        feedback = self.engine.generate_feedback(evaluation)
        
        assert "Criterion A" in feedback
        assert "Criterion B" in feedback
        assert "Good understanding" in feedback
        assert "Needs more detail" in feedback
