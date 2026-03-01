"""Import all models for Alembic discovery."""
from app.models.base import Base
from app.models.user import User
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.concept import Concept
from app.models.assignment import Assignment
from app.models.attempt import Attempt
from app.models.mastery import Mastery

# Export Base for Alembic
__all__ = ["Base"]
