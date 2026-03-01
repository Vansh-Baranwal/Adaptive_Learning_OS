"""Property-based tests and unit tests for security utilities."""
import pytest
from hypothesis import given, strategies as st
from datetime import timedelta, datetime
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



# ============================================================================
# Unit Tests for Edge Cases
# ============================================================================

class TestPasswordHashingEdgeCases:
    """Unit tests for password hashing edge cases."""
    
    def test_empty_password(self):
        """Test hashing an empty password."""
        password = ""
        hashed = hash_password(password)
        assert hashed != password
        assert verify_password(password, hashed)
    
    def test_very_long_password(self):
        """Test hashing a very long password (>72 bytes, bcrypt limit)."""
        password = "a" * 200
        # Bcrypt truncates passwords to 72 bytes, so we test that it works
        # and that the first 72 bytes are what matters
        hashed = hash_password(password)
        assert verify_password(password, hashed)
        # Verify that only first 72 bytes matter (bcrypt behavior)
        assert verify_password("a" * 72, hashed)
    
    def test_special_characters_password(self):
        """Test hashing password with special characters."""
        password = "P@ssw0rd!#$%^&*()_+-=[]{}|;:',.<>?/~`"
        hashed = hash_password(password)
        assert verify_password(password, hashed)
    
    def test_unicode_password(self):
        """Test hashing password with unicode characters."""
        password = "пароль密码🔒"
        hashed = hash_password(password)
        assert verify_password(password, hashed)
    
    def test_wrong_password_verification(self):
        """Test that wrong password fails verification."""
        password = "correct_password"
        wrong_password = "wrong_password"
        hashed = hash_password(password)
        assert not verify_password(wrong_password, hashed)
    
    def test_case_sensitive_password(self):
        """Test that password verification is case-sensitive."""
        password = "Password123"
        hashed = hash_password(password)
        assert not verify_password("password123", hashed)
        assert not verify_password("PASSWORD123", hashed)


class TestJWTEdgeCases:
    """Unit tests for JWT token edge cases."""
    
    def test_expired_token(self):
        """Test that expired tokens are rejected."""
        data = {"user_id": 1, "role": "student"}
        # Create token that expires immediately
        token = create_access_token(data, expires_delta=timedelta(seconds=-1))
        decoded = decode_access_token(token)
        assert decoded is None, "Expired token should be rejected"
    
    def test_token_with_custom_expiration(self):
        """Test creating token with custom expiration time."""
        data = {"user_id": 1, "role": "student"}
        custom_delta = timedelta(minutes=60)
        token = create_access_token(data, expires_delta=custom_delta)
        decoded = decode_access_token(token)
        assert decoded is not None
        assert decoded["user_id"] == 1
    
    def test_malformed_token(self):
        """Test that malformed tokens are rejected."""
        malformed_tokens = [
            "not.a.token",
            "invalid",
            "",
            "a.b",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.signature",
        ]
        for token in malformed_tokens:
            decoded = decode_access_token(token)
            assert decoded is None, f"Malformed token '{token}' should be rejected"
    
    def test_token_with_empty_data(self):
        """Test creating token with empty data."""
        data = {}
        token = create_access_token(data)
        decoded = decode_access_token(token)
        assert decoded is not None
        assert "exp" in decoded
    
    def test_token_with_complex_data(self):
        """Test creating token with complex nested data."""
        data = {
            "user_id": 123,
            "role": "teacher",
            "permissions": ["read", "write", "delete"],
            "metadata": {"department": "Math", "level": 5}
        }
        token = create_access_token(data)
        decoded = decode_access_token(token)
        assert decoded is not None
        assert decoded["user_id"] == 123
        assert decoded["role"] == "teacher"
        assert decoded["permissions"] == ["read", "write", "delete"]
        assert decoded["metadata"]["department"] == "Math"
    
    def test_token_without_expiration_delta(self):
        """Test creating token without explicit expiration (uses default)."""
        data = {"user_id": 1, "role": "student"}
        token = create_access_token(data)
        decoded = decode_access_token(token)
        assert decoded is not None
        assert "exp" in decoded
        # Verify expiration is in the future
        exp_timestamp = decoded["exp"]
        assert exp_timestamp > datetime.utcnow().timestamp()
    
    def test_tampered_token(self):
        """Test that tampered tokens are rejected."""
        data = {"user_id": 1, "role": "student"}
        token = create_access_token(data)
        # Tamper with the token by changing a character
        tampered_token = token[:-5] + "XXXXX"
        decoded = decode_access_token(tampered_token)
        assert decoded is None, "Tampered token should be rejected"
    
    def test_token_with_none_values(self):
        """Test creating token with None values."""
        data = {"user_id": None, "role": None}
        token = create_access_token(data)
        decoded = decode_access_token(token)
        assert decoded is not None
        assert decoded["user_id"] is None
        assert decoded["role"] is None
