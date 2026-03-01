"""Property-based tests for database schema properties.

This module tests database-level properties including foreign key integrity
and index existence.
"""
import pytest
import uuid
from hypothesis import given, strategies as st, settings
from sqlalchemy import inspect, MetaData
from sqlalchemy.exc import IntegrityError

# Try to import database-related modules
try:
    from app.models.base import Base
    from app.models.user import User
    from app.models.student import Student
    from app.models.teacher import Teacher
    from app.models.concept import Concept
    from app.models.assignment import Assignment
    from app.models.attempt import Attempt
    from app.models.mastery import Mastery
    DB_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    DB_AVAILABLE = False


# Feature: adaptive-learning-os, Property 6: Foreign Key Integrity
@pytest.mark.skipif(not DB_AVAILABLE, reason="Database dependencies not available")
def test_foreign_key_integrity_property(db_session):
    """
    Property 6: Foreign Key Integrity
    
    For any table with foreign key relationships, the foreign keys should be
    properly defined with referential integrity constraints, and orphaned
    records should not be possible.
    
    This test verifies:
    1. Foreign key constraints are defined in the database schema
    2. Attempting to create records with invalid foreign keys fails
    3. Deleting parent records properly handles child records (cascade or restrict)
    
    Validates: Requirements 4.8
    """
    # Use Hypothesis to generate test data within the test function
    @given(
        student_first_name=st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll'))),
        student_last_name=st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll'))),
        concept_name=st.text(min_size=1, max_size=100, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Zs'))),
    )
    @settings(max_examples=100)
    def run_property_test(student_first_name, student_last_name, concept_name):
        # Test 1: Verify foreign key constraints exist in schema
        inspector = inspect(db_session.bind)
        
        # Check Student -> User foreign key
        student_fks = inspector.get_foreign_keys('students')
        assert len(student_fks) > 0, "Student table should have foreign key constraints"
        student_user_fk = next((fk for fk in student_fks if fk['referred_table'] == 'users'), None)
        assert student_user_fk is not None, "Student should have foreign key to User"
        assert 'user_id' in student_user_fk['constrained_columns'], "Student.user_id should be foreign key"
        
        # Check Teacher -> User foreign key
        teacher_fks = inspector.get_foreign_keys('teachers')
        assert len(teacher_fks) > 0, "Teacher table should have foreign key constraints"
        teacher_user_fk = next((fk for fk in teacher_fks if fk['referred_table'] == 'users'), None)
        assert teacher_user_fk is not None, "Teacher should have foreign key to User"
        assert 'user_id' in teacher_user_fk['constrained_columns'], "Teacher.user_id should be foreign key"
        
        # Check Concept -> Concept (self-referential) foreign key
        concept_fks = inspector.get_foreign_keys('concepts')
        concept_prereq_fk = next((fk for fk in concept_fks if fk['referred_table'] == 'concepts'), None)
        if concept_prereq_fk:  # Self-referential FK may be optional
            assert 'prerequisite_id' in concept_prereq_fk['constrained_columns'], "Concept.prerequisite_id should be foreign key"
        
        # Check Assignment foreign keys
        assignment_fks = inspector.get_foreign_keys('assignments')
        assert len(assignment_fks) >= 2, "Assignment should have at least 2 foreign keys (concept_id, teacher_id)"
        assignment_concept_fk = next((fk for fk in assignment_fks if fk['referred_table'] == 'concepts'), None)
        assert assignment_concept_fk is not None, "Assignment should have foreign key to Concept"
        assignment_teacher_fk = next((fk for fk in assignment_fks if fk['referred_table'] == 'teachers'), None)
        assert assignment_teacher_fk is not None, "Assignment should have foreign key to Teacher"
        
        # Check Attempt foreign keys
        attempt_fks = inspector.get_foreign_keys('attempts')
        assert len(attempt_fks) >= 3, "Attempt should have at least 3 foreign keys (student_id, assignment_id, concept_id)"
        attempt_student_fk = next((fk for fk in attempt_fks if fk['referred_table'] == 'students'), None)
        assert attempt_student_fk is not None, "Attempt should have foreign key to Student"
        attempt_assignment_fk = next((fk for fk in attempt_fks if fk['referred_table'] == 'assignments'), None)
        assert attempt_assignment_fk is not None, "Attempt should have foreign key to Assignment"
        attempt_concept_fk = next((fk for fk in attempt_fks if fk['referred_table'] == 'concepts'), None)
        assert attempt_concept_fk is not None, "Attempt should have foreign key to Concept"
        
        # Check Mastery foreign keys
        mastery_fks = inspector.get_foreign_keys('mastery')
        assert len(mastery_fks) >= 2, "Mastery should have at least 2 foreign keys (student_id, concept_id)"
        mastery_student_fk = next((fk for fk in mastery_fks if fk['referred_table'] == 'students'), None)
        assert mastery_student_fk is not None, "Mastery should have foreign key to Student"
        mastery_concept_fk = next((fk for fk in mastery_fks if fk['referred_table'] == 'concepts'), None)
        assert mastery_concept_fk is not None, "Mastery should have foreign key to Concept"
        
        # Test 2: Verify that creating records with invalid foreign keys fails
        # Try to create a Student with non-existent user_id
        invalid_student = Student(
            user_id=999999,  # Non-existent user
            first_name=student_first_name,
            last_name=student_last_name
        )
        db_session.add(invalid_student)
        
        with pytest.raises(IntegrityError):
            db_session.commit()
        
        db_session.rollback()
        
        # Test 3: Verify proper cascade behavior
        # Create a valid user and student
        unique_id = str(uuid.uuid4())[:8]
        user = User(
            email=f"test_{unique_id}@example.com",
            hashed_password="hashed_password_here",
            role="student",
            is_active=True
        )
        db_session.add(user)
        db_session.flush()  # Get user.id
        
        student = Student(
            user_id=user.id,
            first_name=student_first_name,
            last_name=student_last_name
        )
        db_session.add(student)
        db_session.flush()  # Get student.id
        
        # Create a concept
        concept = Concept(
            name=f"concept_{unique_id}",
            description="Test concept",
            difficulty_level=1
        )
        db_session.add(concept)
        db_session.flush()  # Get concept.id
        
        # Create a mastery record
        mastery = Mastery(
            student_id=student.id,
            concept_id=concept.id,
            p_l=0.5,
            p_t=0.1,
            p_g=0.25,
            p_s=0.1
        )
        db_session.add(mastery)
        db_session.commit()
        
        # Verify records exist
        assert db_session.query(User).filter_by(id=user.id).first() is not None
        assert db_session.query(Student).filter_by(id=student.id).first() is not None
        assert db_session.query(Mastery).filter_by(student_id=student.id, concept_id=concept.id).first() is not None
        
        # Delete the user (should cascade to student and mastery due to cascade settings)
        db_session.delete(user)
        db_session.commit()
        
        # Verify cascade deletion worked
        assert db_session.query(User).filter_by(id=user.id).first() is None, "User should be deleted"
        assert db_session.query(Student).filter_by(id=student.id).first() is None, "Student should be cascade deleted"
        assert db_session.query(Mastery).filter_by(student_id=student.id).first() is None, "Mastery should be cascade deleted"
        
        # Concept should still exist (not cascade deleted)
        assert db_session.query(Concept).filter_by(id=concept.id).first() is not None, "Concept should still exist"
    
    # Run the property test
    run_property_test()


@pytest.mark.skipif(not DB_AVAILABLE, reason="Database dependencies not available")
def test_foreign_key_constraints_defined():
    """
    Unit test to verify all expected foreign key constraints are defined.
    
    This complements the property test by checking the complete set of
    foreign key relationships in the schema.
    """
    # Get all model classes
    models = [User, Student, Teacher, Concept, Assignment, Attempt, Mastery]
    
    # Verify Base metadata contains all tables
    table_names = [model.__tablename__ for model in models]
    metadata_tables = Base.metadata.tables.keys()
    
    for table_name in table_names:
        assert table_name in metadata_tables, f"Table {table_name} should be in metadata"
    
    # Verify specific foreign key relationships exist in model definitions
    # Student -> User
    assert hasattr(Student, 'user_id'), "Student should have user_id column"
    assert hasattr(Student, 'user'), "Student should have user relationship"
    
    # Teacher -> User
    assert hasattr(Teacher, 'user_id'), "Teacher should have user_id column"
    assert hasattr(Teacher, 'user'), "Teacher should have user relationship"
    
    # Concept -> Concept (self-referential)
    assert hasattr(Concept, 'prerequisite_id'), "Concept should have prerequisite_id column"
    assert hasattr(Concept, 'prerequisite'), "Concept should have prerequisite relationship"
    
    # Assignment -> Concept, Teacher
    assert hasattr(Assignment, 'concept_id'), "Assignment should have concept_id column"
    assert hasattr(Assignment, 'teacher_id'), "Assignment should have teacher_id column"
    assert hasattr(Assignment, 'concept'), "Assignment should have concept relationship"
    assert hasattr(Assignment, 'teacher'), "Assignment should have teacher relationship"
    
    # Attempt -> Student, Assignment, Concept
    assert hasattr(Attempt, 'student_id'), "Attempt should have student_id column"
    assert hasattr(Attempt, 'assignment_id'), "Attempt should have assignment_id column"
    assert hasattr(Attempt, 'concept_id'), "Attempt should have concept_id column"
    assert hasattr(Attempt, 'student'), "Attempt should have student relationship"
    assert hasattr(Attempt, 'assignment'), "Attempt should have assignment relationship"
    assert hasattr(Attempt, 'concept'), "Attempt should have concept relationship"
    
    # Mastery -> Student, Concept
    assert hasattr(Mastery, 'student_id'), "Mastery should have student_id column"
    assert hasattr(Mastery, 'concept_id'), "Mastery should have concept_id column"
    assert hasattr(Mastery, 'student'), "Mastery should have student relationship"
    assert hasattr(Mastery, 'concept'), "Mastery should have concept relationship"
