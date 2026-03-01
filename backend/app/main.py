"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Create FastAPI app
app = FastAPI(
    title="ALOS API",
    description="Adaptive Learning OS - Predictive Mastery Intelligence Platform",
    version="1.0.0"
)

# Configure CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and register routers (will be added in Phase 4)
# from app.api.v1 import auth, students, teachers, concepts, assignments, attempts, mastery
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
# app.include_router(students.router, prefix="/api/v1/students", tags=["students"])
# app.include_router(teachers.router, prefix="/api/v1/teachers", tags=["teachers"])
# app.include_router(concepts.router, prefix="/api/v1/concepts", tags=["concepts"])
# app.include_router(assignments.router, prefix="/api/v1/assignments", tags=["assignments"])
# app.include_router(attempts.router, prefix="/api/v1/attempts", tags=["attempts"])
# app.include_router(mastery.router, prefix="/api/v1/mastery", tags=["mastery"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "ALOS API",
        "version": "1.0.0",
        "status": "Phase 1 Complete - Core Infrastructure Ready"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
