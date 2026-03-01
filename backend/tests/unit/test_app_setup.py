"""Unit tests for application setup (CORS, exception handlers, router registration)."""
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


class TestCORSConfiguration:
    """Test CORS middleware configuration."""
    
    def test_cors_allows_configured_origins(self):
        """Test that CORS allows requests from configured origins."""
        client = TestClient(app)
        
        # Test with allowed origin
        response = client.get(
            "/health",
            headers={"Origin": "http://localhost:3000"}
        )
        
        # Check CORS headers are present
        assert "access-control-allow-origin" in response.headers
        assert response.headers["access-control-allow-origin"] in [
            "http://localhost:3000",
            "*"  # Depending on configuration
        ]
    
    def test_cors_allows_credentials(self):
        """Test that CORS allows credentials."""
        client = TestClient(app)
        
        response = client.options(
            "/api/v1/auth/login",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST"
            }
        )
        
        # Check credentials are allowed
        assert "access-control-allow-credentials" in response.headers
        assert response.headers["access-control-allow-credentials"] == "true"
    
    def test_cors_allows_all_methods(self):
        """Test that CORS allows all HTTP methods."""
        client = TestClient(app)
        
        response = client.options(
            "/api/v1/concepts/",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST"
            }
        )
        
        # Check methods are allowed
        assert "access-control-allow-methods" in response.headers
        allowed_methods = response.headers["access-control-allow-methods"]
        assert "POST" in allowed_methods or "*" in allowed_methods
    
    def test_cors_allows_all_headers(self):
        """Test that CORS allows all headers."""
        client = TestClient(app)
        
        response = client.options(
            "/api/v1/auth/login",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "authorization,content-type"
            }
        )
        
        # Check headers are allowed
        assert "access-control-allow-headers" in response.headers
        allowed_headers = response.headers["access-control-allow-headers"].lower()
        assert "authorization" in allowed_headers or "*" in allowed_headers


class TestExceptionHandlers:
    """Test custom exception handlers."""
    
    def test_authentication_error_handler(self):
        """Test AuthenticationError returns 401 with correct format."""
        client = TestClient(app)
        
        # Create a route that raises AuthenticationError for testing
        @app.get("/test/auth-error")
        async def test_auth_error():
            raise AuthenticationError("Invalid credentials")
        
        response = client.get("/test/auth-error")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "error" in response.json()
        assert "code" in response.json()["error"]
        assert "message" in response.json()["error"]
        assert response.json()["error"]["message"] == "Invalid credentials"
        assert "WWW-Authenticate" in response.headers
    
    def test_authorization_error_handler(self):
        """Test AuthorizationError returns 403 with correct format."""
        client = TestClient(app)
        
        # Create a route that raises AuthorizationError for testing
        @app.get("/test/authz-error")
        async def test_authz_error():
            raise AuthorizationError("Insufficient permissions")
        
        response = client.get("/test/authz-error")
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "error" in response.json()
        assert "code" in response.json()["error"]
        assert "message" in response.json()["error"]
        assert response.json()["error"]["message"] == "Insufficient permissions"
    
    def test_resource_not_found_error_handler(self):
        """Test ResourceNotFoundError returns 404 with correct format."""
        client = TestClient(app)
        
        # Create a route that raises ResourceNotFoundError for testing
        @app.get("/test/not-found-error")
        async def test_not_found_error():
            raise ResourceNotFoundError("Resource not found")
        
        response = client.get("/test/not-found-error")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "error" in response.json()
        assert "code" in response.json()["error"]
        assert "message" in response.json()["error"]
        assert response.json()["error"]["message"] == "Resource not found"
    
    def test_validation_error_handler(self):
        """Test ValidationError returns 422 with correct format."""
        client = TestClient(app)
        
        # Create a route that raises ValidationError for testing
        @app.get("/test/validation-error")
        async def test_validation_error():
            raise ValidationError("Invalid input data")
        
        response = client.get("/test/validation-error")
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "error" in response.json()
        assert "code" in response.json()["error"]
        assert "message" in response.json()["error"]
        assert response.json()["error"]["message"] == "Invalid input data"
    
    def test_database_error_handler(self):
        """Test DatabaseError returns 500 with correct format."""
        client = TestClient(app)
        
        # Create a route that raises DatabaseError for testing
        @app.get("/test/database-error")
        async def test_database_error():
            raise DatabaseError("Database connection failed")
        
        response = client.get("/test/database-error")
        
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "error" in response.json()
        assert "code" in response.json()["error"]
        assert "message" in response.json()["error"]
        assert response.json()["error"]["message"] == "Database connection failed"
    
    def test_generic_alos_exception_handler(self):
        """Test generic ALOSException returns 500 with correct format."""
        client = TestClient(app)
        
        # Create a route that raises ALOSException for testing
        @app.get("/test/generic-error")
        async def test_generic_error():
            raise ALOSException("Generic error occurred")
        
        response = client.get("/test/generic-error")
        
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "error" in response.json()
        assert "code" in response.json()["error"]
        assert "message" in response.json()["error"]
        assert response.json()["error"]["message"] == "Generic error occurred"
    
    def test_error_response_format_consistency(self):
        """Test that all error responses follow the same format."""
        client = TestClient(app)
        
        # Test multiple error types
        @app.get("/test/auth-error-format")
        async def test_auth_error_format():
            raise AuthenticationError("Test auth error")
        
        @app.get("/test/authz-error-format")
        async def test_authz_error_format():
            raise AuthorizationError("Test authz error")
        
        responses = [
            client.get("/test/auth-error-format"),
            client.get("/test/authz-error-format")
        ]
        
        for response in responses:
            data = response.json()
            assert "error" in data
            assert "code" in data["error"]
            assert "message" in data["error"]
            assert "details" in data["error"]
            assert isinstance(data["error"]["details"], dict)


class TestRouterRegistration:
    """Test that all routers are properly registered with correct prefixes."""
    
    def test_auth_router_registered_with_prefix(self):
        """Test that auth router is registered with /api/v1 prefix."""
        client = TestClient(app)
        
        # Test that routes are accessible with prefix
        response = client.post("/api/v1/auth/register", json={})
        assert response.status_code != status.HTTP_404_NOT_FOUND
        
        # Test that routes are NOT accessible without prefix
        response = client.post("/auth/register", json={})
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_students_router_registered_with_prefix(self):
        """Test that students router is registered with /api/v1 prefix."""
        client = TestClient(app)
        
        response = client.get("/api/v1/students/1/mastery")
        assert response.status_code != status.HTTP_404_NOT_FOUND
        
        response = client.get("/students/1/mastery")
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_teachers_router_registered_with_prefix(self):
        """Test that teachers router is registered with /api/v1 prefix."""
        client = TestClient(app)
        
        response = client.get("/api/v1/teachers/1/analytics")
        assert response.status_code != status.HTTP_404_NOT_FOUND
        
        response = client.get("/teachers/1/analytics")
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_concepts_router_registered_with_prefix(self):
        """Test that concepts router is registered with /api/v1 prefix."""
        client = TestClient(app)
        
        response = client.post("/api/v1/concepts/", json={})
        assert response.status_code != status.HTTP_404_NOT_FOUND
        
        response = client.post("/concepts/", json={})
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_assignments_router_registered_with_prefix(self):
        """Test that assignments router is registered with /api/v1 prefix."""
        client = TestClient(app)
        
        # Test POST endpoint instead of GET to avoid NotImplementedError
        response = client.post("/api/v1/assignments/", json={})
        assert response.status_code != status.HTTP_404_NOT_FOUND
        
        response = client.post("/assignments/", json={})
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_attempts_router_registered_with_prefix(self):
        """Test that attempts router is registered with /api/v1 prefix."""
        client = TestClient(app)
        
        response = client.post("/api/v1/attempts/", json={})
        assert response.status_code != status.HTTP_404_NOT_FOUND
        
        response = client.post("/attempts/", json={})
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_mastery_router_registered_with_prefix(self):
        """Test that mastery router is registered with /api/v1 prefix."""
        client = TestClient(app)
        
        response = client.get("/api/v1/mastery/student/1/concept/1")
        assert response.status_code != status.HTTP_404_NOT_FOUND
        
        response = client.get("/mastery/student/1/concept/1")
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_all_routers_count(self):
        """Test that all expected routers are registered."""
        # Get all routes from the app
        routes = [route for route in app.routes]
        
        # Filter API v1 routes
        api_v1_routes = [route for route in routes if hasattr(route, 'path') and route.path.startswith('/api/v1')]
        
        # Verify we have routes from all modules
        route_paths = [route.path for route in api_v1_routes]
        
        # Check for presence of routes from each router
        assert any('/api/v1/auth' in path for path in route_paths), "Auth routes not found"
        assert any('/api/v1/students' in path for path in route_paths), "Student routes not found"
        assert any('/api/v1/teachers' in path for path in route_paths), "Teacher routes not found"
        assert any('/api/v1/concepts' in path for path in route_paths), "Concept routes not found"
        assert any('/api/v1/assignments' in path for path in route_paths), "Assignment routes not found"
        assert any('/api/v1/attempts' in path for path in route_paths), "Attempt routes not found"
        assert any('/api/v1/mastery' in path for path in route_paths), "Mastery routes not found"
    
    def test_health_check_endpoint_registered(self):
        """Test that health check endpoint is registered."""
        client = TestClient(app)
        
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
        assert "status" in response.json()
        assert response.json()["status"] == "healthy"
    
    def test_root_endpoint_registered(self):
        """Test that root endpoint is registered."""
        client = TestClient(app)
        
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json()
        assert "version" in response.json()
        assert "docs" in response.json()
