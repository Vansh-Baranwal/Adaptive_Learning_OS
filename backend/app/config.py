"""Configuration management for ALOS."""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/alos_db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Adaptive Learning OS"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
