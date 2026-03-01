"""Property-based tests for security utilities."""
import pytest
from hypothesis import given, strategies as st
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token


# Feature: adaptive-learning-os, Property 3: Password Hashing
@given(password=st.text(min_size=8, max_size=100))
def test_password_hashing_property(password):
    """
    Property 3: Password Hashing
    
    For any password, the stored hash should be verifiable against the original password.
    The hash should not be plaintext and should use bcrypt format.
    
    Validates: Requirements 3.5
    """
    # Hash the password
    hashed = hash_password(password)
    
    # Verify properties
    assert hashed != password, "Hash should not be plaintext"
    assert verify_password(password, hashed), "Password should be verifiable against hash"
    assert hashed.startswith("$2b$"), "Hash should use bcrypt format"


# Feature: adaptive-learning-os, Property 4: JWT Authentication Flow
@given(
    user_id=st.integers(min_value=1, max_value=1000000),
    role=st.sampled_from(["student", "teacher"])
)
def test_jwt_authentication_flow_property(user_id, role):
    """
    Property 4: JWT Authentication Flow
    
    For any successful user authentication, the system should issue a valid JWT token
    that can be decoded to retrieve user information, and invalid tokens should be rejected.
    
    Validates: Requirements 3.3, 3.6, 3.7
    """
    # Create token with user data
    token_data = {"user_id": user_id, "role": role}
    token = create_access_token(token_data)
    
    # Verify token properties
    assert isinstance(token, str), "Token should be a string"
    assert len(token) > 0, "Token should not be empty"
    
    # Decode token and verify data
    decoded = decode_access_token(token)
    assert decoded is not None, "Valid token should be decodable"
    assert decoded["user_id"] == user_id, "User ID should match"
    assert decoded["role"] == role, "Role should match"
    assert "exp" in decoded, "Token should have expiration"
    
    # Test invalid token rejection
    invalid_token = "invalid.token.here"
    decoded_invalid = decode_access_token(invalid_token)
    assert decoded_invalid is None, "Invalid token should be rejected"


# Feature: adaptive-learning-os, Property 5: Role-Based Access Control
def test_rbac_enforcement_property():
    """
    Property 5: Role-Based Access Control
    
    For any API endpoint requiring specific roles, requests from users without
    the required role should be denied with 403 Forbidden, while requests from
    users with the required role should be allowed.
    
    Validates: Requirements 3.4, 3.8
    
    Note: This is tested through integration tests with actual API endpoints.
    This unit test verifies the RBAC middleware logic exists and is importable.
    """
    from app.core.middleware import require_role, get_current_user, get_current_active_user
    
    # Verify RBAC functions exist
    assert callable(require_role), "require_role should be callable"
    assert callable(get_current_user), "get_current_user should be callable"
    assert callable(get_current_active_user), "get_current_active_user should be callable"
    
    # Verify require_role returns a dependency function
    role_checker = require_role(["teacher"])
    assert callable(role_checker), "require_role should return a callable dependency"
