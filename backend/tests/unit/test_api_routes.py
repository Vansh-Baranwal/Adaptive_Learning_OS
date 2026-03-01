"""Unit tests for API routes."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from app.models.user import User
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.concept import Concept
from app.models.assignment import Assignment
from app.models.attempt import Attempt
from app.models.mastery import Mastery
from datetime import datetime


class TestRouteRegistration:
    """Test that all routes are properly registered."""
    
    def test_auth_routes_registered(self):
        """Test that authentication routes are registered."""
        client = TestClient(app)
        
        # Test /auth/register endpoint exists
        response = client.post("/api/v1/auth/register", json={})
        assert response.status_code != status.HTTP_404_NOT_FOUND
        
        # Test /auth/login endpoint exists
        response = client.post("/api/v1/auth/login", data={})
        assert response.status_code != status.HTTP_404_NOT_FOUND
        
        # Test /auth/me endpoint exists
        response = client.get("/api/v1/auth/me")
        assert response.status_code != status.HTTP_404_NOT_FOUND
    
    def test_student_routes_registered(self):
        """Test that student routes are registered."""
        client = TestClient(app)
        
        # Test student mastery endpoint exists
        response = client.get("/api/v1/students/1/mastery")
        assert response.status_code != status.HTTP_404_NOT_FOUND
        
        # Test student attempts endpoint exists
        response = client.get("/api/v1/students/1/attempts")
        assert response.status_code != status.HTTP_404_NOT_FOUND
    
    def test_teacher_routes_registered(self):
        """Test that teacher routes are registered."""
        client = TestClient(app)
        
        # Test teacher analytics endpoint exists
        response = client.get("/api/v1/teachers/1/analytics")
        assert response.status_code != status.HTTP_404_NOT_FOUND
        
        # Test weak concepts endpoint exists
        response = client.get("/api/v1/teachers/1/students/weak-concepts")
        assert response.status_code != status.HTTP_404_NOT_FOUND
    
    def test_concept_routes_registered(self):
        """Test that concept routes are registered."""
        client = TestClient(app)
        
        # Test create concept endpoint exists
        response = client.post("/api/v1/concepts/", json={})
        assert response.status_code != status.HTTP_404_NOT_FOUND
        
        # Test prerequisites endpoint exists
        response = client.get("/api/v1/concepts/1/prerequisites")
        assert response.status_code != status.HTTP_404_NOT_FOUND
        
        # Test dependents endpoint exists
        response = client.get("/api/v1/concepts/1/dependents")
        assert response.status_code != status.HTTP_404_NOT_FOUND
    
    def test_assignment_routes_registered(self):
        """Test that assignment routes are registered."""
        client = TestClient(app)
        
        # Test create assignment endpoint exists
        response = client.post("/api/v1/assignments/", json={})
        assert response.status_code != status.HTTP_404_NOT_FOUND
        
        # Test get assignment endpoint exists
        response = client.get("/api/v1/assignments/1")
        assert response.status_code != status.HTTP_404_NOT_FOUND
        
        # Test list assignments endpoint exists
        response = client.get("/api/v1/assignments/")
        assert response.status_code != status.HTTP_404_NOT_FOUND
        
        # Test update assignment endpoint exists
        response = client.put("/api/v1/assignments/1", json={})
        assert response.status_code != status.HTTP_404_NOT_FOUND
        
        # Test delete assignment endpoint exists
        response = client.delete("/api/v1/assignments/1")
        assert response.status_code != status.HTTP_404_NOT_FOUND
    
    def test_attempt_routes_registered(self):
        """Test that attempt routes are registered."""
        client = TestClient(app)
        
        # Test submit attempt endpoint exists
        response = client.post("/api/v1/attempts/", json={})
        assert response.status_code != status.HTTP_404_NOT_FOUND
        
        # Test get attempt endpoint exists
        response = client.get("/api/v1/attempts/1")
        assert response.status_code != status.HTTP_404_NOT_FOUND
    
    def test_mastery_routes_registered(self):
        """Test that mastery routes are registered."""
        client = TestClient(app)
        
        # Test get mastery endpoint exists
        response = client.get("/api/v1/mastery/student/1/concept/1")
        assert response.status_code != status.HTTP_404_NOT_FOUND
        
        # Test weak concepts endpoint exists
        response = client.get("/api/v1/mastery/student/1/weak-concepts")
        assert response.status_code != status.HTTP_404_NOT_FOUND
        
        # Test predict mastery endpoint exists
        response = client.get("/api/v1/mastery/student/1/predict/1")
        assert response.status_code != status.HTTP_404_NOT_FOUND


class TestRBACEnforcement:
    """Test that RBAC is properly enforced on protected routes."""
    
    def test_create_concept_requires_teacher_role(self):
        """Test that creating concepts requires teacher role."""
        client = TestClient(app)
        
        # Mock a student user
        student_user = User(id=1, email="student@test.com", role="student", hashed_password="hash", is_active=True)
        
        with patch("app.core.middleware.get_current_user", return_value=student_user):
            response = client.post("/api/v1/concepts/", json={
                "name": "Test Concept",
                "description": "Test",
                "difficulty_level": 1
            })
            # Should be forbidden for students
            assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_create_assignment_requires_teacher_role(self):
        """Test that creating assignments requires teacher role."""
        client = TestClient(app)
        
        # Mock a student user
        student_user = User(id=1, email="student@test.com", role="student", hashed_password="hash", is_active=True)
        
        with patch("app.core.middleware.get_current_user", return_value=student_user):
            response = client.post("/api/v1/assignments/", json={
                "concept_id": 1,
                "title": "Test Assignment",
                "description": "Test"
            })
            # Should be forbidden for students
            assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_submit_attempt_requires_student_role(self):
        """Test that submitting attempts requires student role."""
        client = TestClient(app)
        
        # Mock a teacher user
        teacher_user = User(id=1, email="teacher@test.com", role="teacher", hashed_password="hash", is_active=True)
        
        with patch("app.core.middleware.get_current_user", return_value=teacher_user):
            response = client.post("/api/v1/attempts/", json={
                "student_id": 1,
                "assignment_id": 1,
                "content": "Test answer"
            })
            # Should be forbidden for teachers
            assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_teacher_analytics_requires_teacher_role(self):
        """Test that accessing teacher analytics requires teacher role."""
        client = TestClient(app)
        
        # Mock a student user
        student_user = User(id=1, email="student@test.com", role="student", hashed_password="hash", is_active=True)
        
        with patch("app.core.middleware.get_current_user", return_value=student_user):
            response = client.get("/api/v1/teachers/1/analytics")
            # Should be forbidden for students
            assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_student_mastery_allows_teacher_and_student(self):
        """Test that student mastery endpoint allows both teacher and student roles."""
        client = TestClient(app)
        
        # Test with teacher user
        teacher_user = User(id=1, email="teacher@test.com", role="teacher", hashed_password="hash", is_active=True)
        
        with patch("app.core.middleware.get_current_user", return_value=teacher_user):
            with patch("app.dependencies.get_mastery_service") as mock_service:
                mock_service.return_value.get_all_student_mastery.return_value = []
                response = client.get("/api/v1/students/1/mastery")
                # Should not be forbidden for teachers
                assert response.status_code != status.HTTP_403_FORBIDDEN
        
        # Test with student user (accessing their own data)
        student_user = User(id=2, email="student@test.com", role="student", hashed_password="hash", is_active=True)
        mock_student = Student(id=1, user_id=2, first_name="Test", last_name="Student")
        
        with patch("app.core.middleware.get_current_user", return_value=student_user):
            with patch("app.dependencies.get_student_service") as mock_student_service:
                with patch("app.dependencies.get_mastery_service") as mock_mastery_service:
                    mock_student_service.return_value.get_student_by_user_id.return_value = mock_student
                    mock_mastery_service.return_value.get_all_student_mastery.return_value = []
                    response = client.get("/api/v1/students/1/mastery")
                    # Should not be forbidden for students accessing their own data
                    assert response.status_code != status.HTTP_403_FORBIDDEN
    
    def test_update_assignment_requires_teacher_role(self):
        """Test that updating assignments requires teacher role."""
        client = TestClient(app)
        
        # Mock a student user
        student_user = User(id=1, email="student@test.com", role="student", hashed_password="hash", is_active=True)
        
        with patch("app.core.middleware.get_current_user", return_value=student_user):
            response = client.put("/api/v1/assignments/1", json={
                "concept_id": 1,
                "title": "Updated Assignment",
                "description": "Updated"
            })
            # Should be forbidden for students
            assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_delete_assignment_requires_teacher_role(self):
        """Test that deleting assignments requires teacher role."""
        client = TestClient(app)
        
        # Mock a student user
        student_user = User(id=1, email="student@test.com", role="student", hashed_password="hash", is_active=True)
        
        with patch("app.core.middleware.get_current_user", return_value=student_user):
            response = client.delete("/api/v1/assignments/1")
            # Should be forbidden for students
            assert response.status_code == status.HTTP_403_FORBIDDEN


class TestServiceDelegation:
    """Test that routes properly delegate to service layer."""
    
    def test_register_delegates_to_auth_service(self):
        """Test that register route delegates to AuthService."""
        client = TestClient(app)
        
        mock_user = User(
            id=1,
            email="test@test.com",
            role="student",
            hashed_password="hash",
            is_active=True,
            created_at=datetime.utcnow()
        )
        
        with patch("app.dependencies.get_auth_service") as mock_get_service:
            mock_service = Mock()
            mock_service.register_user.return_value = mock_user
            mock_get_service.return_value = mock_service
            
            response = client.post("/api/v1/auth/register", json={
                "email": "test@test.com",
                "password": "password123",
                "role": "student",
                "first_name": "Test",
                "last_name": "User"
            })
            
            # Verify service method was called
            mock_service.register_user.assert_called_once()
    
    def test_login_delegates_to_auth_service(self):
        """Test that login route delegates to AuthService."""
        client = TestClient(app)
        
        mock_user = User(id=1, email="test@test.com", role="student", hashed_password="hash", is_active=True)
        
        with patch("app.dependencies.get_auth_service") as mock_get_service:
            mock_service = Mock()
            mock_service.authenticate_user.return_value = mock_user
            mock_service.create_access_token.return_value = "test_token"
            mock_get_service.return_value = mock_service
            
            response = client.post("/api/v1/auth/login", data={
                "username": "test@test.com",
                "password": "password123"
            })
            
            # Verify service methods were called
            mock_service.authenticate_user.assert_called_once()
            mock_service.create_access_token.assert_called_once()
    
    def test_create_concept_delegates_to_concept_service(self):
        """Test that create concept route delegates to ConceptService."""
        client = TestClient(app)
        
        teacher_user = User(id=1, email="teacher@test.com", role="teacher", hashed_password="hash", is_active=True)
        mock_concept = Concept(
            id=1,
            name="Test Concept",
            description="Test",
            difficulty_level=1,
            created_at=datetime.utcnow()
        )
        
        with patch("app.core.middleware.get_current_user", return_value=teacher_user):
            with patch("app.dependencies.get_concept_service") as mock_get_service:
                mock_service = Mock()
                mock_service.create_concept.return_value = mock_concept
                mock_get_service.return_value = mock_service
                
                response = client.post("/api/v1/concepts/", json={
                    "name": "Test Concept",
                    "description": "Test",
                    "difficulty_level": 1
                })
                
                # Verify service method was called
                mock_service.create_concept.assert_called_once()
    
    def test_get_student_mastery_delegates_to_mastery_service(self):
        """Test that get student mastery route delegates to MasteryService."""
        client = TestClient(app)
        
        teacher_user = User(id=1, email="teacher@test.com", role="teacher", hashed_password="hash", is_active=True)
        
        with patch("app.core.middleware.get_current_user", return_value=teacher_user):
            with patch("app.dependencies.get_mastery_service") as mock_get_service:
                mock_service = Mock()
                mock_service.get_all_student_mastery.return_value = []
                mock_get_service.return_value = mock_service
                
                response = client.get("/api/v1/students/1/mastery")
                
                # Verify service method was called
                mock_service.get_all_student_mastery.assert_called_once_with(1)
    
    def test_submit_attempt_delegates_to_attempt_service(self):
        """Test that submit attempt route delegates to AttemptService."""
        client = TestClient(app)
        
        student_user = User(id=1, email="student@test.com", role="student", hashed_password="hash", is_active=True)
        mock_attempt = Attempt(
            id=1,
            student_id=1,
            assignment_id=1,
            content="Test answer",
            score=0.8,
            submitted_at=datetime.utcnow()
        )
        
        with patch("app.core.middleware.get_current_user", return_value=student_user):
            with patch("app.dependencies.get_attempt_service") as mock_get_service:
                mock_service = Mock()
                mock_service.submit_attempt.return_value = mock_attempt
                mock_get_service.return_value = mock_service
                
                response = client.post("/api/v1/attempts/", json={
                    "student_id": 1,
                    "assignment_id": 1,
                    "content": "Test answer"
                })
                
                # Verify service method was called
                mock_service.submit_attempt.assert_called_once()
    
    def test_create_assignment_delegates_to_assignment_service(self):
        """Test that create assignment route delegates to AssignmentService."""
        client = TestClient(app)
        
        teacher_user = User(id=1, email="teacher@test.com", role="teacher", hashed_password="hash", is_active=True)
        mock_assignment = Assignment(
            id=1,
            concept_id=1,
            teacher_id=1,
            title="Test Assignment",
            description="Test",
            created_at=datetime.utcnow()
        )
        
        with patch("app.core.middleware.get_current_user", return_value=teacher_user):
            with patch("app.dependencies.get_assignment_service") as mock_get_service:
                mock_service = Mock()
                mock_service.create_assignment.return_value = mock_assignment
                mock_get_service.return_value = mock_service
                
                response = client.post("/api/v1/assignments/", json={
                    "concept_id": 1,
                    "title": "Test Assignment",
                    "description": "Test"
                })
                
                # Verify service method was called
                mock_service.create_assignment.assert_called_once()
    
    def test_get_weak_concepts_delegates_to_mastery_service(self):
        """Test that get weak concepts route delegates to MasteryService."""
        client = TestClient(app)
        
        teacher_user = User(id=1, email="teacher@test.com", role="teacher", hashed_password="hash", is_active=True)
        
        with patch("app.core.middleware.get_current_user", return_value=teacher_user):
            with patch("app.dependencies.get_mastery_service") as mock_get_service:
                mock_service = Mock()
                mock_service.get_weak_concepts.return_value = []
                mock_get_service.return_value = mock_service
                
                response = client.get("/api/v1/mastery/student/1/weak-concepts")
                
                # Verify service method was called
                mock_service.get_weak_concepts.assert_called_once()
    
    def test_get_prerequisites_delegates_to_concept_service(self):
        """Test that get prerequisites route delegates to ConceptService."""
        client = TestClient(app)
        
        with patch("app.dependencies.get_concept_service") as mock_get_service:
            mock_service = Mock()
            mock_service.get_prerequisites.return_value = []
            mock_get_service.return_value = mock_service
            
            response = client.get("/api/v1/concepts/1/prerequisites")
            
            # Verify service method was called
            mock_service.get_prerequisites.assert_called_once_with(1)
    
    def test_teacher_analytics_delegates_to_teacher_service(self):
        """Test that teacher analytics route delegates to TeacherService."""
        client = TestClient(app)
        
        teacher_user = User(id=1, email="teacher@test.com", role="teacher", hashed_password="hash", is_active=True)
        
        with patch("app.core.middleware.get_current_user", return_value=teacher_user):
            with patch("app.dependencies.get_teacher_service") as mock_get_service:
                mock_service = Mock()
                mock_service.get_analytics.return_value = {}
                mock_get_service.return_value = mock_service
                
                response = client.get("/api/v1/teachers/1/analytics")
                
                # Verify service method was called
                mock_service.get_analytics.assert_called_once_with(1)
