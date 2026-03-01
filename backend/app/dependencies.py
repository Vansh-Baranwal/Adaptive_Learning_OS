"""Dependency injection setup for ALOS."""
from typing import Generator
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.ai.mastery_engine import MasteryEngine
from app.ai.readiness import ReadinessEngine
from app.ai.concept_graph import ConceptGraph
from app.ai.rubric_engine import RubricEngine
from app.services.mastery_service import MasteryService
from app.services.auth_service import AuthService
from app.services.student_service import StudentService
from app.services.teacher_service import TeacherService
from app.services.concept_service import ConceptService
from app.services.assignment_service import AssignmentService
from app.services.attempt_service import AttemptService


def get_db() -> Generator[Session, None, None]:
    """
    Get database session.
    
    Yields:
        Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_mastery_engine() -> MasteryEngine:
    """Get MasteryEngine instance."""
    return MasteryEngine()


def get_concept_graph() -> ConceptGraph:
    """Get ConceptGraph instance."""
    return ConceptGraph()


def get_readiness_engine(concept_graph: ConceptGraph = None) -> ReadinessEngine:
    """Get ReadinessEngine instance."""
    if concept_graph is None:
        concept_graph = get_concept_graph()
    return ReadinessEngine(concept_graph)


def get_rubric_engine() -> RubricEngine:
    """Get RubricEngine instance."""
    return RubricEngine()


def get_mastery_service(db: Session) -> MasteryService:
    """Get MasteryService instance."""
    mastery_engine = get_mastery_engine()
    return MasteryService(db, mastery_engine)


def get_auth_service(db: Session) -> AuthService:
    """Get AuthService instance."""
    return AuthService(db)


def get_student_service(db: Session) -> StudentService:
    """Get StudentService instance."""
    return StudentService(db)


def get_teacher_service(db: Session) -> TeacherService:
    """Get TeacherService instance."""
    return TeacherService(db)


def get_concept_service(db: Session) -> ConceptService:
    """Get ConceptService instance."""
    concept_graph = get_concept_graph()
    return ConceptService(db, concept_graph)


def get_assignment_service(db: Session) -> AssignmentService:
    """Get AssignmentService instance."""
    rubric_engine = get_rubric_engine()
    return AssignmentService(db, rubric_engine)


def get_attempt_service(db: Session) -> AttemptService:
    """Get AttemptService instance."""
    mastery_service = get_mastery_service(db)
    return AttemptService(db, mastery_service)
