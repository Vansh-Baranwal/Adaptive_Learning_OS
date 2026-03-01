"""Base model class for SQLAlchemy."""
from sqlalchemy.ext.declarative import declarative_base

# Create declarative base
Base = declarative_base()

# Import all models here for Alembic discovery
# This ensures Alembic can detect all models when generating migrations
