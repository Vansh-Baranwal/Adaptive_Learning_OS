"""Unit tests for exception handling."""
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from app.core.exceptions import (
    ALOSException,
    AuthenticationError,
    AuthorizationError,
    ResourceNotFoundError,
    ValidationError,
    DatabaseError
)


class TestExceptionHierarchy:
    """Test exception class hierarchy."""
    
    def test_alos_exception_is_base_exception(self):
        """Test that ALOSException inherits from Exception."""
        exc = ALOSException("Test message")
        assert isinstance(exc, Exception)
        assert exc.message == "Test message"
        assert exc.code == "ALOS_ERROR"
    
    def test_alos_exception_with_custom_code(self):
        """Test ALOSException with custom error code."""
        exc = ALOSException("Test message", code="CUSTOM_ERROR")
        assert exc.message == "Test message"
        assert exc.code == "CUSTOM_ERROR"
    
    def test_authentication_error_inherits_from_alos_exception(self):
        """Test that AuthenticationError inherits from ALOSException."""
        exc = AuthenticationError()
        assert isinstance(exc, ALOSException)
        assert isinstance(exc, Exception)
        assert exc.code == "AUTHENTICATION_ERROR"
    
    def test_authentication_error_default_message(self):
        """Test AuthenticationError default message."""
        exc = AuthenticationError()
        assert exc.message == "Authentication failed"
    
    def test_authentication_error_custom_message(self):
        """Test AuthenticationError with custom message."""
        exc = AuthenticationError("Invalid credentials")
        assert exc.message == "Invalid credentials"
        assert exc.code == "AUTHENTICATION_ERROR"
    
    def test_authorization_error_inherits_from_alos_exception(self):
        """Test that AuthorizationError inherits from ALOSException."""
        exc = AuthorizationError()
        assert isinstance(exc, ALOSException)
        assert isinstance(exc, Exception)
        assert exc.code == "AUTHORIZATION_ERROR"
    
    def test_authorization_error_default_message(self):
        """Test AuthorizationError default message."""
        exc = AuthorizationError()
        assert exc.message == "Insufficient permissions"
    
    def test_authorization_error_custom_message(self):
        """Test AuthorizationError with custom message."""
        exc = AuthorizationError("Teacher role required")
        assert exc.message == "Teacher role required"
        assert exc.code == "AUTHORIZATION_ERROR"
    
    def test_resource_not_found_error_inherits_from_alos_exception(self):
        """Test that ResourceNotFoundError inherits from ALOSException."""
        exc = ResourceNotFoundError()
        assert isinstance(exc, ALOSException)
        assert isinstance(exc, Exception)
        assert exc.code == "RESOURCE_NOT_FOUND"
    
    def test_resource_not_found_error_default_message(self):
        """Test ResourceNotFoundError default message."""
        exc = ResourceNotFoundError()
        assert exc.message == "Resource not found"
    
    def test_resource_not_found_error_custom_message(self):
        """Test ResourceNotFoundError with custom message."""
        exc = ResourceNotFoundError("Student with ID 123 not found")
        assert exc.message == "Student with ID 123 not found"
        assert exc.code == "RESOURCE_NOT_FOUND"
    
    def test_validation_error_inherits_from_alos_exception(self):
        """Test that ValidationError inherits from ALOSException."""
        exc = ValidationError()
        assert isinstance(exc, ALOSException)
        assert isinstance(exc, Exception)
        assert exc.code == "VALIDATION_ERROR"
    
    def test_validation_error_default_message(self):
        """Test ValidationError default message."""
        exc = ValidationError()
        assert exc.message == "Validation failed"
    
    def test_validation_error_custom_message(self):
        """Test ValidationError with custom message."""
        exc = ValidationError("Email format is invalid")
        assert exc.message == "Email format is invalid"
        assert exc.code == "VALIDATION_ERROR"
    
    def test_database_error_inherits_from_alos_exception(self):
        """Test that DatabaseError inherits from ALOSException."""
        exc = DatabaseError()
        assert isinstance(exc, ALOSException)
        assert isinstance(exc, Exception)
        assert exc.code == "DATABASE_ERROR"
    
    def test_database_error_default_message(self):
        """Test DatabaseError default message."""
        exc = DatabaseError()
        assert exc.message == "Database operation failed"
    
    def test_database_error_custom_message(self):
        """Test DatabaseError with custom message."""
        exc = DatabaseError("Connection timeout")
        assert exc.message == "Connection timeout"
        assert exc.code == "DATABASE_ERROR"
    
    def test_all_exceptions_have_unique_codes(self):
        """Test that all exception types have unique error codes."""
        codes = {
            AuthenticationError().code,
            AuthorizationError().code,
            ResourceNotFoundError().code,
            ValidationError().code,
            DatabaseError().code
        }
        assert len(codes) == 5  # All codes should be unique


class TestErrorResponseFormat:
    """Test error response format from exception handlers."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    def test_authentication_error_response_format(self, client):
        """Test AuthenticationError returns correct response format."""
        # Create a test endpoint that raises AuthenticationError
        @app.get("/test/auth-error")
        async def test_auth_error():
            raise AuthenticationError("Invalid token")
        
        response = client.get("/test/auth-error")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "error" in response.json()
        error = response.json()["error"]
        assert error["code"] == "AUTHENTICATION_ERROR"
        assert error["message"] == "Invalid token"
        assert "details" in error
        assert isinstance(error["details"], dict)
        assert "WWW-Authenticate" in response.headers
    
    def test_authorization_error_response_format(self, client):
        """Test AuthorizationError returns correct response format."""
        @app.get("/test/authz-error")
        async def test_authz_error():
            raise AuthorizationError("Teacher role required")
        
        response = client.get("/test/authz-error")
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "error" in response.json()
        error = response.json()["error"]
        assert error["code"] == "AUTHORIZATION_ERROR"
        assert error["message"] == "Teacher role required"
        assert "details" in error
        assert isinstance(error["details"], dict)
    
    def test_resource_not_found_error_response_format(self, client):
        """Test ResourceNotFoundError returns correct response format."""
        @app.get("/test/not-found-error")
        async def test_not_found_error():
            raise ResourceNotFoundError("Student with ID 123 not found")
        
        response = client.get("/test/not-found-error")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "error" in response.json()
        error = response.json()["error"]
        assert error["code"] == "RESOURCE_NOT_FOUND"
        assert error["message"] == "Student with ID 123 not found"
        assert "details" in error
        assert isinstance(error["details"], dict)
    
    def test_validation_error_response_format(self, client):
        """Test ValidationError returns correct response format."""
        @app.get("/test/validation-error")
        async def test_validation_error():
            raise ValidationError("Email format is invalid")
        
        response = client.get("/test/validation-error")
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "error" in response.json()
        error = response.json()["error"]
        assert error["code"] == "VALIDATION_ERROR"
        assert error["message"] == "Email format is invalid"
        assert "details" in error
        assert isinstance(error["details"], dict)
    
    def test_database_error_response_format(self, client):
        """Test DatabaseError returns correct response format."""
        @app.get("/test/database-error")
        async def test_database_error():
            raise DatabaseError("Connection timeout")
        
        response = client.get("/test/database-error")
        
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "error" in response.json()
        error = response.json()["error"]
        assert error["code"] == "DATABASE_ERROR"
        assert error["message"] == "Connection timeout"
        assert "details" in error
        assert isinstance(error["details"], dict)
    
    def test_generic_alos_exception_response_format(self, client):
        """Test generic ALOSException returns correct response format."""
        @app.get("/test/generic-error")
        async def test_generic_error():
            raise ALOSException("Generic error", code="GENERIC_ERROR")
        
        response = client.get("/test/generic-error")
        
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "error" in response.json()
        error = response.json()["error"]
        assert error["code"] == "GENERIC_ERROR"
        assert error["message"] == "Generic error"
        assert "details" in error
        assert isinstance(error["details"], dict)
    
    def test_error_response_has_required_fields(self, client):
        """Test that all error responses have required fields."""
        @app.get("/test/error-fields")
        async def test_error_fields():
            raise ResourceNotFoundError("Test")
        
        response = client.get("/test/error-fields")
        data = response.json()
        
        # Check top-level structure
        assert "error" in data
        assert len(data) == 1  # Only "error" key
        
        # Check error object structure
        error = data["error"]
        assert "code" in error
        assert "message" in error
        assert "details" in error
        assert len(error) == 3  # Only these three keys
        
        # Check field types
        assert isinstance(error["code"], str)
        assert isinstance(error["message"], str)
        assert isinstance(error["details"], dict)
    
    def test_error_response_details_is_empty_dict(self, client):
        """Test that error response details field is an empty dict."""
        @app.get("/test/empty-details")
        async def test_empty_details():
            raise ValidationError("Test error")
        
        response = client.get("/test/empty-details")
        error = response.json()["error"]
        
        assert error["details"] == {}
        assert len(error["details"]) == 0
