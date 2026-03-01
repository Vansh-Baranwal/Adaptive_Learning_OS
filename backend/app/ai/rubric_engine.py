"""Rubric Engine - Evaluates student work against rubrics."""
from typing import Dict, List


class RubricEngine:
    """Evaluates student work against rubrics."""
    
    def __init__(self):
        """Initialize the rubric engine."""
        pass
    
    def evaluate(self, attempt_content: str, rubric: Dict) -> Dict:
        """
        Evaluate attempt against rubric.
        
        This is a simple rule-based evaluation system. In production, this could
        be enhanced with AI-powered evaluation (e.g., using LLMs).
        
        Rubric format:
        {
            "criteria": [
                {
                    "name": "Criterion name",
                    "max_points": 10,
                    "keywords": ["keyword1", "keyword2"],  # Optional
                    "min_length": 50  # Optional
                }
            ],
            "total_points": 100
        }
        
        Args:
            attempt_content: Student's submitted work
            rubric: Evaluation rubric with criteria
            
        Returns:
            Evaluation results with scores and feedback:
            {
                "total_score": float,
                "max_score": float,
                "percentage": float,
                "criteria_scores": [
                    {
                        "criterion": str,
                        "score": float,
                        "max_score": float,
                        "feedback": str
                    }
                ]
            }
        """
        if not rubric or "criteria" not in rubric:
            # No rubric provided, return default score
            return {
                "total_score": 0.0,
                "max_score": 100.0,
                "percentage": 0.0,
                "criteria_scores": []
            }
        
        criteria = rubric.get("criteria", [])
        total_points = rubric.get("total_points", 100)
        
        criteria_scores = []
        total_score = 0.0
        
        # Evaluate each criterion
        for criterion in criteria:
            criterion_name = criterion.get("name", "Unnamed criterion")
            max_points = criterion.get("max_points", 10)
            keywords = criterion.get("keywords", [])
            min_length = criterion.get("min_length", 0)
            
            # Calculate score for this criterion
            score, feedback = self._evaluate_criterion(
                attempt_content, 
                criterion_name,
                max_points,
                keywords,
                min_length
            )
            
            criteria_scores.append({
                "criterion": criterion_name,
                "score": score,
                "max_score": max_points,
                "feedback": feedback
            })
            
            total_score += score
        
        # Calculate percentage
        max_score = sum(c.get("max_points", 0) for c in criteria)
        if max_score == 0:
            max_score = total_points
        
        percentage = (total_score / max_score * 100) if max_score > 0 else 0.0
        
        return {
            "total_score": total_score,
            "max_score": max_score,
            "percentage": percentage,
            "criteria_scores": criteria_scores
        }
    
    def _evaluate_criterion(
        self, 
        content: str, 
        criterion_name: str,
        max_points: float,
        keywords: List[str],
        min_length: int
    ) -> tuple[float, str]:
        """
        Evaluate a single criterion.
        
        Args:
            content: Student's work
            criterion_name: Name of criterion
            max_points: Maximum points for this criterion
            keywords: Keywords to look for
            min_length: Minimum required length
            
        Returns:
            Tuple of (score, feedback)
        """
        score = 0.0
        feedback_parts = []
        
        # Check length requirement
        if min_length > 0:
            if len(content) >= min_length:
                score += max_points * 0.3  # 30% for meeting length
                feedback_parts.append("Meets length requirement")
            else:
                feedback_parts.append(f"Content too short (minimum {min_length} characters)")
        else:
            # If no length requirement, give base points
            score += max_points * 0.3
        
        # Check for keywords
        if keywords:
            content_lower = content.lower()
            found_keywords = [kw for kw in keywords if kw.lower() in content_lower]
            keyword_ratio = len(found_keywords) / len(keywords)
            
            keyword_score = max_points * 0.7 * keyword_ratio  # 70% for keywords
            score += keyword_score
            
            if found_keywords:
                feedback_parts.append(f"Found key concepts: {', '.join(found_keywords)}")
            else:
                feedback_parts.append("Missing key concepts")
        else:
            # If no keywords specified, give remaining points
            score += max_points * 0.7
        
        # Ensure score doesn't exceed max
        score = min(score, max_points)
        
        feedback = "; ".join(feedback_parts) if feedback_parts else "Evaluated"
        
        return score, feedback
    
    def generate_feedback(self, evaluation: Dict) -> str:
        """
        Generate human-readable feedback from evaluation.
        
        Args:
            evaluation: Evaluation results from evaluate()
            
        Returns:
            Formatted feedback string
        """
        if not evaluation:
            return "No evaluation data available."
        
        total_score = evaluation.get("total_score", 0)
        max_score = evaluation.get("max_score", 100)
        percentage = evaluation.get("percentage", 0)
        criteria_scores = evaluation.get("criteria_scores", [])
        
        # Build feedback message
        feedback_lines = []
        feedback_lines.append(f"Overall Score: {total_score:.1f}/{max_score:.1f} ({percentage:.1f}%)")
        feedback_lines.append("")
        
        # Add criterion-specific feedback
        if criteria_scores:
            feedback_lines.append("Detailed Feedback:")
            for i, criterion_score in enumerate(criteria_scores, 1):
                criterion = criterion_score.get("criterion", "Unknown")
                score = criterion_score.get("score", 0)
                max_pts = criterion_score.get("max_score", 0)
                feedback = criterion_score.get("feedback", "")
                
                feedback_lines.append(f"{i}. {criterion}: {score:.1f}/{max_pts:.1f}")
                if feedback:
                    feedback_lines.append(f"   {feedback}")
        
        # Add overall assessment
        feedback_lines.append("")
        if percentage >= 90:
            feedback_lines.append("Excellent work! You've demonstrated strong understanding.")
        elif percentage >= 80:
            feedback_lines.append("Good work! You've shown solid understanding.")
        elif percentage >= 70:
            feedback_lines.append("Satisfactory work. Consider reviewing the material.")
        elif percentage >= 60:
            feedback_lines.append("Needs improvement. Please review the concepts.")
        else:
            feedback_lines.append("Significant improvement needed. Please seek additional help.")
        
        return "\n".join(feedback_lines)
