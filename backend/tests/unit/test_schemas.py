"""Unit tests for Pydantic schemas."""
import pytest
from datetime import datetime
from pydantic import ValidationError
from app.schemas.user import UserBase, UserCreate, UserResponse, Token, TokenData
from app.schemas.student import StudentBase, StudentCreate, StudentResponse
from app.schemas.teacher import TeacherBase, TeacherCreate, TeacherResponse
from app.schemas.concept import ConceptBase, ConceptCreate, ConceptResponse
from app.schemas.assignment import AssignmentBase, AssignmentCreate, AssignmentResponse
from app.schemas.attempt import AttemptBase, AttemptCreate, AttemptResponse
from app.schemas.mastery import MasteryBase, MasteryResponse


class TestUserSchemas:
    """Test User schema validation and serialization."""
    
    def test_user_base_valid(self):
        """Test UserBase with valid data."""
        user = UserBase(email="test@example.com", role="student")
        assert user.email == "test@example.com"
        assert user.role == "student"
    
    def test_user_base_invalid_email(self):
        """Test UserBase rejects invalid email."""
        with pytest.raises(ValidationError) as exc_info:
            UserBase(email="invalid-email", role="student")
        assert "email" in str(exc_info.value).lower()
    
    def test_user_base_invalid_role(self):
        """Test UserBase rejects invalid role."""
        with pytest.raises(ValidationError) as exc_info:
            UserBase(email="test@example.com", role="admin")
        assert "role" in str(exc_info.value).lower()
    
    def test_user_create_valid(self):
        """Test UserCreate with valid data."""
        user = UserCreate(
            email="student@example.com",
            role="student",
            password="securepass123",
            first_name="John",
            last_name="Doe"
        )
        assert user.email == "student@example.com"
        assert user.password == "securepass123"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.department is None
    
    def test_user_create_with_department(self):
        """Test UserCreate with department for teacher."""
        user = UserCreate(
            email="teacher@example.com",
            role="teacher",
            password="securepass123",
            first_name="Jane",
            last_name="Smith",
            department="Mathematics"
        )
        assert user.department == "Mathematics"
    
    def test_user_create_missing_required_fields(self):
        """Test UserCreate rejects missing required fields."""
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(email="test@example.com", role="student")
        errors = str(exc_info.value).lower()
        assert "password" in errors or "first_name" in errors or "last_name" in errors
    
    def test_user_response_serialization(self):
        """Test UserResponse serialization."""
        now = datetime.utcnow()
        user = UserResponse(
            email="test@example.com",
            role="student",
            id=1,
            is_active=True,
            created_at=now
        )
        assert user.id == 1
        assert user.is_active is True
        assert user.created_at == now
    
    def test_token_schema(self):
        """Test Token schema."""
        token = Token(access_token="abc123xyz")
        assert token.access_token == "abc123xyz"
        assert token.token_type == "bearer"
    
    def test_token_custom_type(self):
        """Test Token with custom token_type."""
        token = Token(access_token="abc123", token_type="custom")
        assert token.token_type == "custom"
    
    def test_token_data_schema(self):
        """Test TokenData schema."""
        token_data = TokenData(user_id=42, role="teacher")
        assert token_data.user_id == 42
        assert token_data.role == "teacher"


class TestStudentSchemas:
    """Test Student schema validation and serialization."""
    
    def test_student_base_valid(self):
        """Test StudentBase with valid data."""
        student = StudentBase(first_name="Alice", last_name="Johnson")
        assert student.first_name == "Alice"
        assert student.last_name == "Johnson"
    
    def test_student_base_missing_fields(self):
        """Test StudentBase rejects missing required fields."""
        with pytest.raises(ValidationError):
            StudentBase(first_name="Alice")
    
    def test_student_create_valid(self):
        """Test StudentCreate with valid data."""
        student = StudentCreate(first_name="Bob", last_name="Williams")
        assert student.first_name == "Bob"
        assert student.last_name == "Williams"
    
    def test_student_response_serialization(self):
        """Test StudentResponse serialization."""
        now = datetime.utcnow()
        student = StudentResponse(
            first_name="Charlie",
            last_name="Brown",
            id=10,
            user_id=5,
            enrolled_at=now
        )
        assert student.id == 10
        assert student.user_id == 5
        assert student.enrolled_at == now


class TestTeacherSchemas:
    """Test Teacher schema validation and serialization."""
    
    def test_teacher_base_valid(self):
        """Test TeacherBase with valid data."""
        teacher = TeacherBase(
            first_name="David",
            last_name="Miller",
            department="Physics"
        )
        assert teacher.first_name == "David"
        assert teacher.last_name == "Miller"
        assert teacher.department == "Physics"
    
    def test_teacher_base_optional_department(self):
        """Test TeacherBase with optional department."""
        teacher = TeacherBase(first_name="Eve", last_name="Davis")
        assert teacher.department is None
    
    def test_teacher_create_valid(self):
        """Test TeacherCreate with valid data."""
        teacher = TeacherCreate(
            first_name="Frank",
            last_name="Wilson",
            department="Chemistry"
        )
        assert teacher.first_name == "Frank"
        assert teacher.department == "Chemistry"
    
    def test_teacher_response_serialization(self):
        """Test TeacherResponse serialization."""
        teacher = TeacherResponse(
            first_name="Grace",
            last_name="Taylor",
            id=20,
            user_id=15,
            department="Biology"
        )
        assert teacher.id == 20
        assert teacher.user_id == 15
        assert teacher.department == "Biology"


class TestConceptSchemas:
    """Test Concept schema validation and serialization."""
    
    def test_concept_base_valid(self):
        """Test ConceptBase with valid data."""
        concept = ConceptBase(
            name="Derivatives",
            description="Introduction to derivatives",
            difficulty_level=2
        )
        assert concept.name == "Derivatives"
        assert concept.description == "Introduction to derivatives"
        assert concept.difficulty_level == 2
    
    def test_concept_base_defaults(self):
        """Test ConceptBase with default values."""
        concept = ConceptBase(name="Integrals")
        assert concept.name == "Integrals"
        assert concept.description is None
        assert concept.difficulty_level == 1
    
    def test_concept_create_valid(self):
        """Test ConceptCreate with valid data."""
        concept = ConceptCreate(
            name="Limits",
            description="Concept of limits",
            prerequisite_id=5
        )
        assert concept.name == "Limits"
        assert concept.prerequisite_id == 5
    
    def test_concept_create_no_prerequisite(self):
        """Test ConceptCreate without prerequisite."""
        concept = ConceptCreate(name="Algebra Basics")
        assert concept.prerequisite_id is None
    
    def test_concept_response_serialization(self):
        """Test ConceptResponse serialization."""
        now = datetime.utcnow()
        concept = ConceptResponse(
            name="Calculus I",
            description="First calculus course",
            difficulty_level=3,
            id=100,
            prerequisite_id=50,
            created_at=now
        )
        assert concept.id == 100
        assert concept.prerequisite_id == 50
        assert concept.created_at == now


class TestAssignmentSchemas:
    """Test Assignment schema validation and serialization."""
    
    def test_assignment_base_valid(self):
        """Test AssignmentBase with valid data."""
        due = datetime.utcnow()
        assignment = AssignmentBase(
            title="Homework 1",
            description="First homework assignment",
            rubric={"criteria": "accuracy", "points": 100},
            due_date=due
        )
        assert assignment.title == "Homework 1"
        assert assignment.description == "First homework assignment"
        assert assignment.rubric == {"criteria": "accuracy", "points": 100}
        assert assignment.due_date == due
    
    def test_assignment_base_optional_fields(self):
        """Test AssignmentBase with optional fields."""
        assignment = AssignmentBase(title="Quiz 1")
        assert assignment.title == "Quiz 1"
        assert assignment.description is None
        assert assignment.rubric is None
        assert assignment.due_date is None
    
    def test_assignment_create_valid(self):
        """Test AssignmentCreate with valid data."""
        assignment = AssignmentCreate(
            title="Midterm Exam",
            concept_id=10,
            teacher_id=5
        )
        assert assignment.title == "Midterm Exam"
        assert assignment.concept_id == 10
        assert assignment.teacher_id == 5
    
    def test_assignment_create_missing_required_fields(self):
        """Test AssignmentCreate rejects missing required fields."""
        with pytest.raises(ValidationError):
            AssignmentCreate(title="Test")
    
    def test_assignment_response_serialization(self):
        """Test AssignmentResponse serialization."""
        now = datetime.utcnow()
        assignment = AssignmentResponse(
            title="Final Exam",
            id=200,
            concept_id=15,
            teacher_id=8,
            created_at=now
        )
        assert assignment.id == 200
        assert assignment.concept_id == 15
        assert assignment.teacher_id == 8
        assert assignment.created_at == now


class TestAttemptSchemas:
    """Test Attempt schema validation and serialization."""
    
    def test_attempt_base_valid(self):
        """Test AttemptBase with valid data."""
        attempt = AttemptBase(content="My detailed answer to the question")
        assert attempt.content == "My detailed answer to the question"
    
    def test_attempt_base_missing_content(self):
        """Test AttemptBase rejects missing content."""
        with pytest.raises(ValidationError):
            AttemptBase()
    
    def test_attempt_create_valid(self):
        """Test AttemptCreate with valid data."""
        attempt = AttemptCreate(
            content="Solution to problem 1",
            student_id=25,
            assignment_id=30,
            concept_id=12
        )
        assert attempt.content == "Solution to problem 1"
        assert attempt.student_id == 25
        assert attempt.assignment_id == 30
        assert attempt.concept_id == 12
    
    def test_attempt_create_missing_required_fields(self):
        """Test AttemptCreate rejects missing required fields."""
        with pytest.raises(ValidationError):
            AttemptCreate(content="Answer", student_id=1)
    
    def test_attempt_response_serialization(self):
        """Test AttemptResponse serialization."""
        now = datetime.utcnow()
        attempt = AttemptResponse(
            content="My submission",
            id=300,
            student_id=40,
            assignment_id=50,
            concept_id=20,
            score=92.5,
            evaluation={"feedback": "Excellent work", "grade": "A"},
            submitted_at=now
        )
        assert attempt.id == 300
        assert attempt.student_id == 40
        assert attempt.assignment_id == 50
        assert attempt.concept_id == 20
        assert attempt.score == 92.5
        assert attempt.evaluation == {"feedback": "Excellent work", "grade": "A"}
        assert attempt.submitted_at == now
    
    def test_attempt_response_optional_fields(self):
        """Test AttemptResponse with optional fields as None."""
        now = datetime.utcnow()
        attempt = AttemptResponse(
            content="Submission",
            id=301,
            student_id=41,
            assignment_id=51,
            concept_id=21,
            submitted_at=now
        )
        assert attempt.score is None
        assert attempt.evaluation is None


class TestMasterySchemas:
    """Test Mastery schema validation and serialization."""
    
    def test_mastery_base_valid(self):
        """Test MasteryBase with valid data."""
        mastery = MasteryBase(
            p_l=0.75,
            p_t=0.15,
            p_g=0.2,
            p_s=0.05,
            attempt_count=10
        )
        assert mastery.p_l == 0.75
        assert mastery.p_t == 0.15
        assert mastery.p_g == 0.2
        assert mastery.p_s == 0.05
        assert mastery.attempt_count == 10
    
    def test_mastery_base_missing_fields(self):
        """Test MasteryBase rejects missing required fields."""
        with pytest.raises(ValidationError):
            MasteryBase(p_l=0.5, p_t=0.1)
    
    def test_mastery_response_serialization(self):
        """Test MasteryResponse serialization."""
        now = datetime.utcnow()
        mastery = MasteryResponse(
            p_l=0.8,
            p_t=0.12,
            p_g=0.25,
            p_s=0.08,
            attempt_count=15,
            id=400,
            student_id=60,
            concept_id=35,
            last_updated=now
        )
        assert mastery.id == 400
        assert mastery.student_id == 60
        assert mastery.concept_id == 35
        assert mastery.p_l == 0.8
        assert mastery.attempt_count == 15
        assert mastery.last_updated == now
    
    def test_mastery_response_bkt_parameters(self):
        """Test MasteryResponse includes all BKT parameters."""
        now = datetime.utcnow()
        mastery = MasteryResponse(
            p_l=0.6,
            p_t=0.1,
            p_g=0.25,
            p_s=0.1,
            attempt_count=5,
            id=401,
            student_id=61,
            concept_id=36,
            last_updated=now
        )
        # Verify all BKT parameters are present
        assert hasattr(mastery, 'p_l')
        assert hasattr(mastery, 'p_t')
        assert hasattr(mastery, 'p_g')
        assert hasattr(mastery, 'p_s')
        assert mastery.p_l == 0.6
        assert mastery.p_t == 0.1
        assert mastery.p_g == 0.25
        assert mastery.p_s == 0.1


class TestSchemaSerializationEdgeCases:
    """Test edge cases for schema serialization."""
    
    def test_empty_string_validation(self):
        """Test schemas reject empty strings where appropriate."""
        with pytest.raises(ValidationError):
            UserBase(email="", role="student")
    
    def test_numeric_field_types(self):
        """Test numeric fields accept correct types."""
        concept = ConceptBase(name="Test", difficulty_level=5)
        assert concept.difficulty_level == 5
        
        # Test float for mastery
        mastery = MasteryBase(p_l=0.5, p_t=0.1, p_g=0.25, p_s=0.1, attempt_count=0)
        assert isinstance(mastery.p_l, float)
    
    def test_datetime_field_serialization(self):
        """Test datetime fields serialize correctly."""
        now = datetime.utcnow()
        user = UserResponse(
            email="test@example.com",
            role="student",
            id=1,
            is_active=True,
            created_at=now
        )
        assert isinstance(user.created_at, datetime)
        assert user.created_at == now
    
    def test_json_field_serialization(self):
        """Test JSON/dict fields serialize correctly."""
        rubric = {"criteria": ["accuracy", "completeness"], "max_points": 100}
        assignment = AssignmentBase(title="Test", rubric=rubric)
        assert assignment.rubric == rubric
        assert isinstance(assignment.rubric, dict)
    
    def test_optional_fields_none_values(self):
        """Test optional fields accept None values."""
        concept = ConceptCreate(name="Test Concept", prerequisite_id=None)
        assert concept.prerequisite_id is None
        
        teacher = TeacherBase(first_name="John", last_name="Doe", department=None)
        assert teacher.department is None
