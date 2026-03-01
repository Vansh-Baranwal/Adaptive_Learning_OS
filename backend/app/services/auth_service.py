"""Authentication Service."""
from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import User
from app.models.student import Student
from app.models.teacher import Teacher
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password, create_access_token
from app.core.exceptions import AuthenticationError, ValidationError


class AuthService:
    """Authentication service for user registration and login."""
    
    def __init__(self, db: Session):
        """
        Initialize authentication service.
        
        Args:
            db: Database session
        """
        self.db = db
    
    def register_user(self, user_data: UserCreate) -> User:
        """
        Register a new user with hashed password.
        
        Args:
            user_data: User registration data
            
        Returns:
            Created user
        """
        # Check if email already exists
        existing = self.db.query(User).filter(User.email == user_data.email).first()
        if existing:
            raise ValidationError("Email already registered")
        
        # Create user with hashed password
        user = User(
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
            role=user_data.role,
            is_active=True,
        )
        self.db.add(user)
        self.db.flush()  # Get user.id before creating student/teacher
        
        # Create associated student or teacher record
        if user_data.role == "student":
            student = Student(
                user_id=user.id,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
            )
            self.db.add(student)
        else:
            teacher = Teacher(
                user_id=user.id,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                department=user_data.department,
            )
            self.db.add(teacher)
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate user credentials.
        
        Args:
            email: User email
            password: Plain text password
            
        Returns:
            User if authentication successful, None otherwise
        """
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    def create_access_token(self, user_id: int, role: str) -> str:
        """
        Generate JWT access token.
        
        Args:
            user_id: User ID
            role: User role
            
        Returns:
            JWT access token
        """
        return create_access_token(data={"user_id": user_id, "role": role})
