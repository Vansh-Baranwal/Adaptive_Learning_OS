"""Unit tests for SQLAlchemy data models."""
import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.concept import Concept
from app.models.assignment import Assignment
from app.models.attempt import Attempt
from app.models.mastery import Mastery


class TestUserModel:
    """Test User model instantiation and relationships."""
    
    def test_user_instantiation(self, db_session):
        """Test that User model can be instantiated with required fields."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            role="student"
        )
        db_session.add(user)
        db_session.commit()
        
        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.hashed_password == "hashed_password_123"
        assert user.role == "student"
        assert user.is_active is True
        assert isinstance(user.created_at, datetime)
    
    def test_user_email_unique_constraint(self, db_session):
        """Test that User email must be unique."""
        user1 = User(email="test@example.com", hashed_password="hash1", role="student")
        user2 = User(email="test@example.com", hashed_password="hash2", role="teacher")
        
        db_session.add(user1)
        db_session.commit()
        
        db_session.add(user2)
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_user_student_relationship(self, db_session):
        """Test User to Student relationship."""
        user = User(email="student@example.com", hashed_password="hash", role="student")
        db_session.add(user)
        db_session.commit()
        
        student = Student(user_id=user.id, first_name="John", last_name="Doe")
        db_session.add(student)
        db_session.commit()
        
        assert user.student is not None
        assert user.student.first_name == "John"
        assert student.user.email == "student@example.com"
    
    def test_user_teacher_relationship(self, db_session):
        """Test User to Teacher relationship."""
        user = User(email="teacher@example.com", hashed_password="hash", role="teacher")
        db_session.add(user)
        db_session.commit()
        
        teacher = Teacher(user_id=user.id, first_name="Jane", last_name="Smith", department="Math")
        db_session.add(teacher)
        db_session.commit()
        
        assert user.teacher is not None
        assert user.teacher.department == "Math"
        assert teacher.user.email == "teacher@example.com"


class TestStudentModel:
    """Test Student model instantiation and relationships."""
    
    def test_student_instantiation(self, db_session):
        """Test that Student model can be instantiated with required fields."""
        user = User(email="student@example.com", hashed_password="hash", role="student")
        db_session.add(user)
        db_session.commit()
        
        student = Student(
            user_id=user.id,
            first_name="Alice",
            last_name="Johnson"
        )
        db_session.add(student)
        db_session.commit()
        
        assert student.id is not None
        assert student.user_id == user.id
        assert student.first_name == "Alice"
        assert student.last_name == "Johnson"
        assert isinstance(student.enrolled_at, datetime)
    
    def test_student_user_id_unique_constraint(self, db_session):
        """Test that Student user_id must be unique."""
        user = User(email="student@example.com", hashed_password="hash", role="student")
        db_session.add(user)
        db_session.commit()
        
        student1 = Student(user_id=user.id, first_name="Alice", last_name="Johnson")
        student2 = Student(user_id=user.id, first_name="Bob", last_name="Smith")
        
        db_session.add(student1)
        db_session.commit()
        
        db_session.add(student2)
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_student_attempts_relationship(self, db_session):
        """Test Student to Attempts relationship."""
        # Create user and student
        user = User(email="student@example.com", hashed_password="hash", role="student")
        db_session.add(user)
        db_session.commit()
        
        student = Student(user_id=user.id, first_name="Alice", last_name="Johnson")
        db_session.add(student)
        db_session.commit()
        
        # Create concept, teacher, and assignment
        concept = Concept(name="Calculus I", description="Basic calculus")
        db_session.add(concept)
        db_session.commit()
        
        teacher_user = User(email="teacher@example.com", hashed_password="hash", role="teacher")
        db_session.add(teacher_user)
        db_session.commit()
        
        teacher = Teacher(user_id=teacher_user.id, first_name="Jane", last_name="Smith")
        db_session.add(teacher)
        db_session.commit()
        
        assignment = Assignment(
            concept_id=concept.id,
            teacher_id=teacher.id,
            title="Quiz 1",
            description="First quiz"
        )
        db_session.add(assignment)
        db_session.commit()
        
        # Create attempt
        attempt = Attempt(
            student_id=student.id,
            assignment_id=assignment.id,
            concept_id=concept.id,
            content="My answer"
        )
        db_session.add(attempt)
        db_session.commit()
        
        assert len(student.attempts) == 1
        assert student.attempts[0].content == "My answer"
    
    def test_student_mastery_relationship(self, db_session):
        """Test Student to Mastery relationship."""
        user = User(email="student@example.com", hashed_password="hash", role="student")
        db_session.add(user)
        db_session.commit()
        
        student = Student(user_id=user.id, first_name="Alice", last_name="Johnson")
        db_session.add(student)
        db_session.commit()
        
        concept = Concept(name="Calculus I", description="Basic calculus")
        db_session.add(concept)
        db_session.commit()
        
        mastery = Mastery(student_id=student.id, concept_id=concept.id, p_l=0.7)
        db_session.add(mastery)
        db_session.commit()
        
        assert len(student.mastery) == 1
        assert student.mastery[0].p_l == 0.7


class TestTeacherModel:
    """Test Teacher model instantiation and relationships."""
    
    def test_teacher_instantiation(self, db_session):
        """Test that Teacher model can be instantiated with required fields."""
        user = User(email="teacher@example.com", hashed_password="hash", role="teacher")
        db_session.add(user)
        db_session.commit()
        
        teacher = Teacher(
            user_id=user.id,
            first_name="Bob",
            last_name="Williams",
            department="Mathematics"
        )
        db_session.add(teacher)
        db_session.commit()
        
        assert teacher.id is not None
        assert teacher.user_id == user.id
        assert teacher.first_name == "Bob"
        assert teacher.last_name == "Williams"
        assert teacher.department == "Mathematics"
    
    def test_teacher_assignments_relationship(self, db_session):
        """Test Teacher to Assignments relationship."""
        user = User(email="teacher@example.com", hashed_password="hash", role="teacher")
        db_session.add(user)
        db_session.commit()
        
        teacher = Teacher(user_id=user.id, first_name="Bob", last_name="Williams")
        db_session.add(teacher)
        db_session.commit()
        
        concept = Concept(name="Calculus I", description="Basic calculus")
        db_session.add(concept)
        db_session.commit()
        
        assignment = Assignment(
            concept_id=concept.id,
            teacher_id=teacher.id,
            title="Homework 1",
            description="First homework"
        )
        db_session.add(assignment)
        db_session.commit()
        
        assert len(teacher.assignments) == 1
        assert teacher.assignments[0].title == "Homework 1"


class TestConceptModel:
    """Test Concept model instantiation and relationships."""
    
    def test_concept_instantiation(self, db_session):
        """Test that Concept model can be instantiated with required fields."""
        concept = Concept(
            name="Derivatives",
            description="Introduction to derivatives",
            difficulty_level=2
        )
        db_session.add(concept)
        db_session.commit()
        
        assert concept.id is not None
        assert concept.name == "Derivatives"
        assert concept.description == "Introduction to derivatives"
        assert concept.difficulty_level == 2
        assert isinstance(concept.created_at, datetime)
    
    def test_concept_name_unique_constraint(self, db_session):
        """Test that Concept name must be unique."""
        concept1 = Concept(name="Calculus", description="First")
        concept2 = Concept(name="Calculus", description="Second")
        
        db_session.add(concept1)
        db_session.commit()
        
        db_session.add(concept2)
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_concept_prerequisite_relationship(self, db_session):
        """Test Concept self-referential prerequisite relationship."""
        prerequisite = Concept(name="Algebra", description="Basic algebra")
        db_session.add(prerequisite)
        db_session.commit()
        
        dependent = Concept(
            name="Calculus",
            description="Requires algebra",
            prerequisite_id=prerequisite.id
        )
        db_session.add(dependent)
        db_session.commit()
        
        assert dependent.prerequisite is not None
        assert dependent.prerequisite.name == "Algebra"
        assert len(prerequisite.dependents) == 1
        assert prerequisite.dependents[0].name == "Calculus"
    
    def test_concept_assignments_relationship(self, db_session):
        """Test Concept to Assignments relationship."""
        concept = Concept(name="Calculus I", description="Basic calculus")
        db_session.add(concept)
        db_session.commit()
        
        user = User(email="teacher@example.com", hashed_password="hash", role="teacher")
        db_session.add(user)
        db_session.commit()
        
        teacher = Teacher(user_id=user.id, first_name="Jane", last_name="Smith")
        db_session.add(teacher)
        db_session.commit()
        
        assignment = Assignment(
            concept_id=concept.id,
            teacher_id=teacher.id,
            title="Quiz 1"
        )
        db_session.add(assignment)
        db_session.commit()
        
        assert len(concept.assignments) == 1
        assert concept.assignments[0].title == "Quiz 1"


class TestAssignmentModel:
    """Test Assignment model instantiation and relationships."""
    
    def test_assignment_instantiation(self, db_session):
        """Test that Assignment model can be instantiated with required fields."""
        concept = Concept(name="Calculus I", description="Basic calculus")
        db_session.add(concept)
        db_session.commit()
        
        user = User(email="teacher@example.com", hashed_password="hash", role="teacher")
        db_session.add(user)
        db_session.commit()
        
        teacher = Teacher(user_id=user.id, first_name="Jane", last_name="Smith")
        db_session.add(teacher)
        db_session.commit()
        
        assignment = Assignment(
            concept_id=concept.id,
            teacher_id=teacher.id,
            title="Midterm Exam",
            description="Comprehensive exam",
            rubric={"criteria": "accuracy"}
        )
        db_session.add(assignment)
        db_session.commit()
        
        assert assignment.id is not None
        assert assignment.concept_id == concept.id
        assert assignment.teacher_id == teacher.id
        assert assignment.title == "Midterm Exam"
        assert assignment.rubric == {"criteria": "accuracy"}
        assert isinstance(assignment.created_at, datetime)
    
    def test_assignment_attempts_relationship(self, db_session):
        """Test Assignment to Attempts relationship."""
        concept = Concept(name="Calculus I", description="Basic calculus")
        db_session.add(concept)
        db_session.commit()
        
        teacher_user = User(email="teacher@example.com", hashed_password="hash", role="teacher")
        db_session.add(teacher_user)
        db_session.commit()
        
        teacher = Teacher(user_id=teacher_user.id, first_name="Jane", last_name="Smith")
        db_session.add(teacher)
        db_session.commit()
        
        assignment = Assignment(
            concept_id=concept.id,
            teacher_id=teacher.id,
            title="Quiz 1"
        )
        db_session.add(assignment)
        db_session.commit()
        
        student_user = User(email="student@example.com", hashed_password="hash", role="student")
        db_session.add(student_user)
        db_session.commit()
        
        student = Student(user_id=student_user.id, first_name="Alice", last_name="Johnson")
        db_session.add(student)
        db_session.commit()
        
        attempt = Attempt(
            student_id=student.id,
            assignment_id=assignment.id,
            concept_id=concept.id,
            content="My submission"
        )
        db_session.add(attempt)
        db_session.commit()
        
        assert len(assignment.attempts) == 1
        assert assignment.attempts[0].content == "My submission"


class TestAttemptModel:
    """Test Attempt model instantiation and relationships."""
    
    def test_attempt_instantiation(self, db_session):
        """Test that Attempt model can be instantiated with required fields."""
        # Create necessary related objects
        concept = Concept(name="Calculus I", description="Basic calculus")
        db_session.add(concept)
        db_session.commit()
        
        teacher_user = User(email="teacher@example.com", hashed_password="hash", role="teacher")
        db_session.add(teacher_user)
        db_session.commit()
        
        teacher = Teacher(user_id=teacher_user.id, first_name="Jane", last_name="Smith")
        db_session.add(teacher)
        db_session.commit()
        
        assignment = Assignment(
            concept_id=concept.id,
            teacher_id=teacher.id,
            title="Quiz 1"
        )
        db_session.add(assignment)
        db_session.commit()
        
        student_user = User(email="student@example.com", hashed_password="hash", role="student")
        db_session.add(student_user)
        db_session.commit()
        
        student = Student(user_id=student_user.id, first_name="Alice", last_name="Johnson")
        db_session.add(student)
        db_session.commit()
        
        # Create attempt
        attempt = Attempt(
            student_id=student.id,
            assignment_id=assignment.id,
            concept_id=concept.id,
            content="My detailed answer",
            score=85.5,
            evaluation={"feedback": "Good work"}
        )
        db_session.add(attempt)
        db_session.commit()
        
        assert attempt.id is not None
        assert attempt.student_id == student.id
        assert attempt.assignment_id == assignment.id
        assert attempt.concept_id == concept.id
        assert attempt.content == "My detailed answer"
        assert attempt.score == 85.5
        assert attempt.evaluation == {"feedback": "Good work"}
        assert isinstance(attempt.submitted_at, datetime)
    
    def test_attempt_relationships(self, db_session):
        """Test Attempt relationships to Student, Assignment, and Concept."""
        # Create necessary related objects
        concept = Concept(name="Calculus I", description="Basic calculus")
        db_session.add(concept)
        db_session.commit()
        
        teacher_user = User(email="teacher@example.com", hashed_password="hash", role="teacher")
        db_session.add(teacher_user)
        db_session.commit()
        
        teacher = Teacher(user_id=teacher_user.id, first_name="Jane", last_name="Smith")
        db_session.add(teacher)
        db_session.commit()
        
        assignment = Assignment(
            concept_id=concept.id,
            teacher_id=teacher.id,
            title="Quiz 1"
        )
        db_session.add(assignment)
        db_session.commit()
        
        student_user = User(email="student@example.com", hashed_password="hash", role="student")
        db_session.add(student_user)
        db_session.commit()
        
        student = Student(user_id=student_user.id, first_name="Alice", last_name="Johnson")
        db_session.add(student)
        db_session.commit()
        
        # Create attempt
        attempt = Attempt(
            student_id=student.id,
            assignment_id=assignment.id,
            concept_id=concept.id,
            content="My answer"
        )
        db_session.add(attempt)
        db_session.commit()
        
        assert attempt.student.first_name == "Alice"
        assert attempt.assignment.title == "Quiz 1"
        assert attempt.concept.name == "Calculus I"


class TestMasteryModel:
    """Test Mastery model instantiation and relationships."""
    
    def test_mastery_instantiation(self, db_session):
        """Test that Mastery model can be instantiated with required fields."""
        student_user = User(email="student@example.com", hashed_password="hash", role="student")
        db_session.add(student_user)
        db_session.commit()
        
        student = Student(user_id=student_user.id, first_name="Alice", last_name="Johnson")
        db_session.add(student)
        db_session.commit()
        
        concept = Concept(name="Calculus I", description="Basic calculus")
        db_session.add(concept)
        db_session.commit()
        
        mastery = Mastery(
            student_id=student.id,
            concept_id=concept.id,
            p_l=0.75,
            p_t=0.15,
            p_g=0.2,
            p_s=0.05,
            attempt_count=5
        )
        db_session.add(mastery)
        db_session.commit()
        
        assert mastery.id is not None
        assert mastery.student_id == student.id
        assert mastery.concept_id == concept.id
        assert mastery.p_l == 0.75
        assert mastery.p_t == 0.15
        assert mastery.p_g == 0.2
        assert mastery.p_s == 0.05
        assert mastery.attempt_count == 5
        assert isinstance(mastery.last_updated, datetime)
    
    def test_mastery_default_values(self, db_session):
        """Test that Mastery model has correct default BKT parameter values."""
        student_user = User(email="student@example.com", hashed_password="hash", role="student")
        db_session.add(student_user)
        db_session.commit()
        
        student = Student(user_id=student_user.id, first_name="Alice", last_name="Johnson")
        db_session.add(student)
        db_session.commit()
        
        concept = Concept(name="Calculus I", description="Basic calculus")
        db_session.add(concept)
        db_session.commit()
        
        mastery = Mastery(student_id=student.id, concept_id=concept.id)
        db_session.add(mastery)
        db_session.commit()
        
        assert mastery.p_l == 0.5
        assert mastery.p_t == 0.1
        assert mastery.p_g == 0.25
        assert mastery.p_s == 0.1
        assert mastery.attempt_count == 0
    
    def test_mastery_unique_constraint(self, db_session):
        """Test that Mastery has unique constraint on (student_id, concept_id)."""
        student_user = User(email="student@example.com", hashed_password="hash", role="student")
        db_session.add(student_user)
        db_session.commit()
        
        student = Student(user_id=student_user.id, first_name="Alice", last_name="Johnson")
        db_session.add(student)
        db_session.commit()
        
        concept = Concept(name="Calculus I", description="Basic calculus")
        db_session.add(concept)
        db_session.commit()
        
        mastery1 = Mastery(student_id=student.id, concept_id=concept.id, p_l=0.6)
        mastery2 = Mastery(student_id=student.id, concept_id=concept.id, p_l=0.8)
        
        db_session.add(mastery1)
        db_session.commit()
        
        db_session.add(mastery2)
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_mastery_relationships(self, db_session):
        """Test Mastery relationships to Student and Concept."""
        student_user = User(email="student@example.com", hashed_password="hash", role="student")
        db_session.add(student_user)
        db_session.commit()
        
        student = Student(user_id=student_user.id, first_name="Alice", last_name="Johnson")
        db_session.add(student)
        db_session.commit()
        
        concept = Concept(name="Calculus I", description="Basic calculus")
        db_session.add(concept)
        db_session.commit()
        
        mastery = Mastery(student_id=student.id, concept_id=concept.id)
        db_session.add(mastery)
        db_session.commit()
        
        assert mastery.student.first_name == "Alice"
        assert mastery.concept.name == "Calculus I"
