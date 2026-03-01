"""Custom exception classes for ALOS."""


class ALOSException(Exception):
    """Base exception for ALOS system."""
    
    def __init__(self, message: str, code: str = "ALOS_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class AuthenticationError(ALOSException):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, code="AUTHENTICATION_ERROR")


class AuthorizationError(ALOSException):
    """Raised when user lacks required permissions."""
    
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, code="AUTHORIZATION_ERROR")


class ResourceNotFoundError(ALOSException):
    """Raised when requested resource doesn't exist."""
    
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, code="RESOURCE_NOT_FOUND")


class ValidationError(ALOSException):
    """Raised when data validation fails."""
    
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, code="VALIDATION_ERROR")


class DatabaseError(ALOSException):
    """Raised when database operations fail."""
    
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(message, code="DATABASE_ERROR")
