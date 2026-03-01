"""Mastery Engine - Bayesian Knowledge Tracing implementation."""
from typing import List, Dict


class MasteryEngine:
    """Handles mastery prediction and updates using Bayesian Knowledge Tracing."""
    
    def __init__(self):
        """Initialize the mastery engine."""
        pass
    
    def predict_mastery(self, student_history: List[Dict], concept_id: int) -> float:
        """
        Predict mastery level for a student-concept pair.
        
        This method applies BKT iteratively over the student's history of attempts
        to predict the current mastery level.
        
        Args:
            student_history: List of past attempts and scores. Each dict should contain:
                - 'correct': bool indicating if attempt was correct
                - 'p_l': float, current mastery probability before this attempt
                - 'p_t': float, learning rate
                - 'p_g': float, guess probability
                - 'p_s': float, slip probability
            concept_id: Target concept ID
            
        Returns:
            Predicted mastery level (0.0 to 1.0)
        """
        if not student_history:
            # No history, return default initial mastery
            return 0.5
        
        # Start with the initial mastery from the first attempt
        current_p_l = student_history[0].get('p_l', 0.5)
        
        # Apply BKT update for each attempt in history
        for attempt in student_history:
            current_p_l = self.update_mastery_belief(
                current_mastery=current_p_l,
                attempt_result=attempt
            )
        
        return current_p_l
    
    def update_mastery_belief(self, current_mastery: float, attempt_result: Dict) -> float:
        """
        Update mastery belief based on new attempt using Bayesian Knowledge Tracing.
        
        BKT Algorithm:
        1. Calculate P(correct | learned) = 1 - p_s
        2. Calculate P(correct | not learned) = p_g
        3. Calculate P(correct) = P(L) * P(correct|L) + P(~L) * P(correct|~L)
        4. Update P(L | observation) using Bayes' rule
        5. Apply learning: P(L_new) = P(L | obs) + (1 - P(L | obs)) * p_t
        
        Args:
            current_mastery: Current mastery level (p_l)
            attempt_result: Result of latest attempt. Dict should contain:
                - 'correct': bool indicating if attempt was correct
                - 'p_t': float, learning rate (probability of learning from attempt)
                - 'p_g': float, guess probability (P(correct | not learned))
                - 'p_s': float, slip probability (P(incorrect | learned))
            
        Returns:
            Updated mastery level (0.0 to 1.0)
        """
        # Extract parameters from attempt_result
        correct = attempt_result.get('correct', False)
        p_t = attempt_result.get('p_t', 0.1)  # Learning rate
        p_g = attempt_result.get('p_g', 0.25)  # Guess probability
        p_s = attempt_result.get('p_s', 0.1)  # Slip probability
        
        # Current probability of mastery
        p_l = current_mastery
        
        # Step 1: Calculate conditional probabilities
        # P(correct | learned) = 1 - p_s (probability of correct answer when learned)
        p_correct_given_learned = 1.0 - p_s
        
        # P(correct | not learned) = p_g (probability of correct answer by guessing)
        p_correct_given_not_learned = p_g
        
        # Step 2: Calculate total probability of correct answer
        # P(correct) = P(L) * P(correct|L) + P(~L) * P(correct|~L)
        p_correct = (p_l * p_correct_given_learned + 
                    (1.0 - p_l) * p_correct_given_not_learned)
        
        # Step 3: Update belief using Bayes' rule
        if correct:
            # P(L | correct) = P(correct | L) * P(L) / P(correct)
            if p_correct > 0:
                p_l_given_obs = (p_correct_given_learned * p_l) / p_correct
            else:
                p_l_given_obs = p_l
        else:
            # P(L | incorrect) = P(incorrect | L) * P(L) / P(incorrect)
            p_incorrect = 1.0 - p_correct
            if p_incorrect > 0:
                p_incorrect_given_learned = p_s
                p_l_given_obs = (p_incorrect_given_learned * p_l) / p_incorrect
            else:
                p_l_given_obs = p_l
        
        # Step 4: Apply learning (student may learn from this attempt)
        # P(L_new) = P(L | obs) + (1 - P(L | obs)) * p_t
        p_l_new = p_l_given_obs + (1.0 - p_l_given_obs) * p_t
        
        # Ensure result is in valid range [0, 1]
        p_l_new = max(0.0, min(1.0, p_l_new))
        
        return p_l_new
