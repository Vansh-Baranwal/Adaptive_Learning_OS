"""Unit tests for service layer structure validation.

Tests that service methods exist with correct signatures and proper dependencies.
Requirements: 5.10, 6.3
"""
import inspect
import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session

from app.services.auth_service import AuthService
from app.services.student_service import StudentService
from app.services.teacher_service import TeacherService
from app.services.concept_service import ConceptService
from app.services.assignment_service import AssignmentService
from app.services.attempt_service import AttemptService
from app.services.mastery_service import MasteryService
from app.ai.mastery_engine import MasteryEngine
from app.ai.concept_graph import ConceptGraph
from app.ai.rubric_engine import RubricEngine


class TestAuthServiceStructure:
    """Test AuthService class structure and method signatures."""
    
    def test_auth_service_class_exists(self):
        """Test that AuthService class exists."""
        assert AuthService is not None, "AuthService class should exist"
    
    def test_auth_service_instantiation(self):
        """Test that AuthService can be instantiated with database session."""
        db = Mock(spec=Session)
        service = AuthService(db)
        assert service is not None, "AuthService should be instantiable"
        assert isinstance(service, AuthService), "Instance should be of type AuthService"
        assert service.db is db, "AuthService should store database session"
    
    def test_register_user_method_exists(self):
        """Test that register_user method exists with correct signature."""
        db = Mock(spec=Session)
        service = AuthService(db)
        assert hasattr(service, 'register_user'), "AuthService should have register_user method"
        
        # Check method signature
        sig = inspect.signature(service.register_user)
        params = list(sig.parameters.keys())
        assert 'user_data' in params, "register_user should have user_data parameter"
    
    def test_authenticate_user_method_exists(self):
        """Test that authenticate_user method exists with correct signature."""
        db = Mock(spec=Session)
        service = AuthService(db)
        assert hasattr(service, 'authenticate_user'), "AuthService should have authenticate_user method"
        
        # Check method signature
        sig = inspect.signature(service.authenticate_user)
        params = list(sig.parameters.keys())
        assert 'email' in params, "authenticate_user should have email parameter"
        assert 'password' in params, "authenticate_user should have password parameter"
    
    def test_create_access_token_method_exists(self):
        """Test that create_access_token method exists with correct signature."""
        db = Mock(spec=Session)
        service = AuthService(db)
        assert hasattr(service, 'create_access_token'), "AuthService should have create_access_token method"
        
        # Check method signature
        sig = inspect.signature(service.create_access_token)
        params = list(sig.parameters.keys())
        assert 'user_id' in params, "create_access_token should have user_id parameter"
        assert 'role' in params, "create_access_token should have role parameter"
    
    def test_auth_service_methods_raise_not_implemented(self):
        """Test that AuthService methods raise NotImplementedError (placeholder)."""
        db = Mock(spec=Session)
        service = AuthService(db)
        
        with pytest.raises(NotImplementedError):
            service.register_user(Mock())
        with pytest.raises(NotImplementedError):
            service.authenticate_user("test@example.com", "password")
        with pytest.raises(NotImplementedError):
            service.create_access_token(1, "student")


class TestStudentServiceStructure:
    """Test StudentService class structure and method signatures."""
    
    def test_student_service_class_exists(self):
        """Test that StudentService class exists."""
        assert StudentService is not None, "StudentService class should exist"
    
    def test_student_service_instantiation(self):
        """Test that StudentService can be instantiated with database session."""
        db = Mock(spec=Session)
        service = StudentService(db)
        assert service is not None, "StudentService should be instantiable"
        assert isinstance(service, StudentService), "Instance should be of type StudentService"
        assert service.db is db, "StudentService should store database session"
    
    def test_get_student_method_exists(self):
        """Test that get_student method exists with correct signature."""
        db = Mock(spec=Session)
        service = StudentService(db)
        assert hasattr(service, 'get_student'), "StudentService should have get_student method"
        
        # Check method signature
        sig = inspect.signature(service.get_student)
        params = list(sig.parameters.keys())
        assert 'student_id' in params, "get_student should have student_id parameter"
    
    def test_get_student_by_user_id_method_exists(self):
        """Test that get_student_by_user_id method exists with correct signature."""
        db = Mock(spec=Session)
        service = StudentService(db)
        assert hasattr(service, 'get_student_by_user_id'), "StudentService should have get_student_by_user_id method"
        
        # Check method signature
        sig = inspect.signature(service.get_student_by_user_id)
        params = list(sig.parameters.keys())
        assert 'user_id' in params, "get_student_by_user_id should have user_id parameter"
    
    def test_student_service_methods_raise_not_implemented(self):
        """Test that StudentService methods raise NotImplementedError (placeholder)."""
        db = Mock(spec=Session)
        service = StudentService(db)
        
        with pytest.raises(NotImplementedError):
            service.get_student(1)
        with pytest.raises(NotImplementedError):
            service.get_student_by_user_id(1)


class TestTeacherServiceStructure:
    """Test TeacherService class structure and method signatures."""
    
    def test_teacher_service_class_exists(self):
        """Test that TeacherService class exists."""
        assert TeacherService is not None, "TeacherService class should exist"
    
    def test_teacher_service_instantiation(self):
        """Test that TeacherService can be instantiated with database session."""
        db = Mock(spec=Session)
        service = TeacherService(db)
        assert service is not None, "TeacherService should be instantiable"
        assert isinstance(service, TeacherService), "Instance should be of type TeacherService"
        assert service.db is db, "TeacherService should store database session"
    
    def test_get_teacher_method_exists(self):
        """Test that get_teacher method exists with correct signature."""
        db = Mock(spec=Session)
        service = TeacherService(db)
        assert hasattr(service, 'get_teacher'), "TeacherService should have get_teacher method"
        
        # Check method signature
        sig = inspect.signature(service.get_teacher)
        params = list(sig.parameters.keys())
        assert 'teacher_id' in params, "get_teacher should have teacher_id parameter"
    
    def test_get_teacher_by_user_id_method_exists(self):
        """Test that get_teacher_by_user_id method exists with correct signature."""
        db = Mock(spec=Session)
        service = TeacherService(db)
        assert hasattr(service, 'get_teacher_by_user_id'), "TeacherService should have get_teacher_by_user_id method"
        
        # Check method signature
        sig = inspect.signature(service.get_teacher_by_user_id)
        params = list(sig.parameters.keys())
        assert 'user_id' in params, "get_teacher_by_user_id should have user_id parameter"
    
    def test_get_class_analytics_method_exists(self):
        """Test that get_class_analytics method exists with correct signature."""
        db = Mock(spec=Session)
        service = TeacherService(db)
        assert hasattr(service, 'get_class_analytics'), "TeacherService should have get_class_analytics method"
        
        # Check method signature
        sig = inspect.signature(service.get_class_analytics)
        params = list(sig.parameters.keys())
        assert 'teacher_id' in params, "get_class_analytics should have teacher_id parameter"
    
    def test_teacher_service_methods_raise_not_implemented(self):
        """Test that TeacherService methods raise NotImplementedError (placeholder)."""
        db = Mock(spec=Session)
        service = TeacherService(db)
        
        with pytest.raises(NotImplementedError):
            service.get_teacher(1)
        with pytest.raises(NotImplementedError):
            service.get_teacher_by_user_id(1)
        with pytest.raises(NotImplementedError):
            service.get_class_analytics(1)


class TestConceptServiceStructure:
    """Test ConceptService class structure and method signatures."""
    
    def test_concept_service_class_exists(self):
        """Test that ConceptService class exists."""
        assert ConceptService is not None, "ConceptService class should exist"
    
    def test_concept_service_instantiation(self):
        """Test that ConceptService can be instantiated with database session and ConceptGraph."""
        db = Mock(spec=Session)
        concept_graph = ConceptGraph()
        service = ConceptService(db, concept_graph)
        assert service is not None, "ConceptService should be instantiable"
        assert isinstance(service, ConceptService), "Instance should be of type ConceptService"
        assert service.db is db, "ConceptService should store database session"
        assert service.concept_graph is concept_graph, "ConceptService should store ConceptGraph"
    
    def test_create_concept_method_exists(self):
        """Test that create_concept method exists with correct signature."""
        db = Mock(spec=Session)
        concept_graph = ConceptGraph()
        service = ConceptService(db, concept_graph)
        assert hasattr(service, 'create_concept'), "ConceptService should have create_concept method"
        
        # Check method signature
        sig = inspect.signature(service.create_concept)
        params = list(sig.parameters.keys())
        assert 'concept_data' in params, "create_concept should have concept_data parameter"
    
    def test_get_prerequisites_method_exists(self):
        """Test that get_prerequisites method exists with correct signature."""
        db = Mock(spec=Session)
        concept_graph = ConceptGraph()
        service = ConceptService(db, concept_graph)
        assert hasattr(service, 'get_prerequisites'), "ConceptService should have get_prerequisites method"
        
        # Check method signature
        sig = inspect.signature(service.get_prerequisites)
        params = list(sig.parameters.keys())
        assert 'concept_id' in params, "get_prerequisites should have concept_id parameter"
    
    def test_get_learning_path_method_exists(self):
        """Test that get_learning_path method exists with correct signature."""
        db = Mock(spec=Session)
        concept_graph = ConceptGraph()
        service = ConceptService(db, concept_graph)
        assert hasattr(service, 'get_learning_path'), "ConceptService should have get_learning_path method"
        
        # Check method signature
        sig = inspect.signature(service.get_learning_path)
        params = list(sig.parameters.keys())
        assert 'student_id' in params, "get_learning_path should have student_id parameter"
        assert 'target_concept_id' in params, "get_learning_path should have target_concept_id parameter"
    
    def test_concept_service_methods_raise_not_implemented(self):
        """Test that ConceptService methods raise NotImplementedError (placeholder)."""
        db = Mock(spec=Session)
        concept_graph = ConceptGraph()
        service = ConceptService(db, concept_graph)
        
        with pytest.raises(NotImplementedError):
            service.create_concept(Mock())
        with pytest.raises(NotImplementedError):
            service.get_prerequisites(1)
        with pytest.raises(NotImplementedError):
            service.get_learning_path(1, 1)


class TestAssignmentServiceStructure:
    """Test AssignmentService class structure and method signatures."""
    
    def test_assignment_service_class_exists(self):
        """Test that AssignmentService class exists."""
        assert AssignmentService is not None, "AssignmentService class should exist"
    
    def test_assignment_service_instantiation(self):
        """Test that AssignmentService can be instantiated with dependencies."""
        db = Mock(spec=Session)
        rubric_engine = RubricEngine()
        mastery_service = Mock(spec=MasteryService)
        service = AssignmentService(db, rubric_engine, mastery_service)
        assert service is not None, "AssignmentService should be instantiable"
        assert isinstance(service, AssignmentService), "Instance should be of type AssignmentService"
        assert service.db is db, "AssignmentService should store database session"
        assert service.rubric_engine is rubric_engine, "AssignmentService should store RubricEngine"
        assert service.mastery_service is mastery_service, "AssignmentService should store MasteryService"
    
    def test_assignment_service_instantiation_without_mastery_service(self):
        """Test that AssignmentService can be instantiated without MasteryService (optional)."""
        db = Mock(spec=Session)
        rubric_engine = RubricEngine()
        service = AssignmentService(db, rubric_engine)
        assert service is not None, "AssignmentService should be instantiable without MasteryService"
        assert service.mastery_service is None, "MasteryService should be None when not provided"
    
    def test_create_assignment_method_exists(self):
        """Test that create_assignment method exists with correct signature."""
        db = Mock(spec=Session)
        rubric_engine = RubricEngine()
        service = AssignmentService(db, rubric_engine)
        assert hasattr(service, 'create_assignment'), "AssignmentService should have create_assignment method"
        
        # Check method signature
        sig = inspect.signature(service.create_assignment)
        params = list(sig.parameters.keys())
        assert 'assignment_data' in params, "create_assignment should have assignment_data parameter"
    
    def test_get_assignment_method_exists(self):
        """Test that get_assignment method exists with correct signature."""
        db = Mock(spec=Session)
        rubric_engine = RubricEngine()
        service = AssignmentService(db, rubric_engine)
        assert hasattr(service, 'get_assignment'), "AssignmentService should have get_assignment method"
        
        # Check method signature
        sig = inspect.signature(service.get_assignment)
        params = list(sig.parameters.keys())
        assert 'assignment_id' in params, "get_assignment should have assignment_id parameter"
    
    def test_submit_assignment_method_exists(self):
        """Test that submit_assignment method exists with correct signature."""
        db = Mock(spec=Session)
        rubric_engine = RubricEngine()
        service = AssignmentService(db, rubric_engine)
        assert hasattr(service, 'submit_assignment'), "AssignmentService should have submit_assignment method"
        
        # Check method signature
        sig = inspect.signature(service.submit_assignment)
        params = list(sig.parameters.keys())
        assert 'assignment_id' in params, "submit_assignment should have assignment_id parameter"
        assert 'student_id' in params, "submit_assignment should have student_id parameter"
        assert 'content' in params, "submit_assignment should have content parameter"
    
    def test_list_assignments_method_exists(self):
        """Test that list_assignments method exists with correct signature."""
        db = Mock(spec=Session)
        rubric_engine = RubricEngine()
        service = AssignmentService(db, rubric_engine)
        assert hasattr(service, 'list_assignments'), "AssignmentService should have list_assignments method"
        
        # Check method signature
        sig = inspect.signature(service.list_assignments)
        params = list(sig.parameters.keys())
        assert 'concept_id' in params, "list_assignments should have concept_id parameter"
    
    def test_assignment_service_methods_raise_not_implemented(self):
        """Test that AssignmentService methods raise NotImplementedError (placeholder)."""
        db = Mock(spec=Session)
        rubric_engine = RubricEngine()
        service = AssignmentService(db, rubric_engine)
        
        with pytest.raises(NotImplementedError):
            service.create_assignment(Mock())
        with pytest.raises(NotImplementedError):
            service.get_assignment(1)
        with pytest.raises(NotImplementedError):
            service.submit_assignment(1, 1, "content")
        with pytest.raises(NotImplementedError):
            service.list_assignments()



class TestAttemptServiceStructure:
    """Test AttemptService class structure and method signatures."""
    
    def test_attempt_service_class_exists(self):
        """Test that AttemptService class exists."""
        assert AttemptService is not None, "AttemptService class should exist"
    
    def test_attempt_service_instantiation(self):
        """Test that AttemptService can be instantiated with dependencies."""
        db = Mock(spec=Session)
        mastery_service = Mock(spec=MasteryService)
        service = AttemptService(db, mastery_service)
        assert service is not None, "AttemptService should be instantiable"
        assert isinstance(service, AttemptService), "Instance should be of type AttemptService"
        assert service.db is db, "AttemptService should store database session"
        assert service.mastery_service is mastery_service, "AttemptService should store MasteryService"
    
    def test_submit_attempt_method_exists(self):
        """Test that submit_attempt method exists with correct signature."""
        db = Mock(spec=Session)
        mastery_service = Mock(spec=MasteryService)
        service = AttemptService(db, mastery_service)
        assert hasattr(service, 'submit_attempt'), "AttemptService should have submit_attempt method"
        
        # Check method signature
        sig = inspect.signature(service.submit_attempt)
        params = list(sig.parameters.keys())
        assert 'attempt_data' in params, "submit_attempt should have attempt_data parameter"
    
    def test_get_attempt_method_exists(self):
        """Test that get_attempt method exists with correct signature."""
        db = Mock(spec=Session)
        mastery_service = Mock(spec=MasteryService)
        service = AttemptService(db, mastery_service)
        assert hasattr(service, 'get_attempt'), "AttemptService should have get_attempt method"
        
        # Check method signature
        sig = inspect.signature(service.get_attempt)
        params = list(sig.parameters.keys())
        assert 'attempt_id' in params, "get_attempt should have attempt_id parameter"
    
    def test_get_student_attempts_method_exists(self):
        """Test that get_student_attempts method exists with correct signature."""
        db = Mock(spec=Session)
        mastery_service = Mock(spec=MasteryService)
        service = AttemptService(db, mastery_service)
        assert hasattr(service, 'get_student_attempts'), "AttemptService should have get_student_attempts method"
        
        # Check method signature
        sig = inspect.signature(service.get_student_attempts)
        params = list(sig.parameters.keys())
        assert 'student_id' in params, "get_student_attempts should have student_id parameter"
        assert 'concept_id' in params, "get_student_attempts should have concept_id parameter"
    
    def test_attempt_service_methods_raise_not_implemented(self):
        """Test that AttemptService methods raise NotImplementedError (placeholder)."""
        db = Mock(spec=Session)
        mastery_service = Mock(spec=MasteryService)
        service = AttemptService(db, mastery_service)
        
        with pytest.raises(NotImplementedError):
            service.submit_attempt(Mock())
        with pytest.raises(NotImplementedError):
            service.get_attempt(1)
        with pytest.raises(NotImplementedError):
            service.get_student_attempts(1)


class TestMasteryServiceStructure:
    """Test MasteryService class structure and method signatures."""
    
    def test_mastery_service_class_exists(self):
        """Test that MasteryService class exists."""
        assert MasteryService is not None, "MasteryService class should exist"
    
    def test_mastery_service_instantiation(self):
        """Test that MasteryService can be instantiated with dependencies."""
        db = Mock(spec=Session)
        mastery_engine = MasteryEngine()
        service = MasteryService(db, mastery_engine)
        assert service is not None, "MasteryService should be instantiable"
        assert isinstance(service, MasteryService), "Instance should be of type MasteryService"
        assert service.db is db, "MasteryService should store database session"
        assert service.mastery_engine is mastery_engine, "MasteryService should store MasteryEngine"
    
    def test_get_student_mastery_method_exists(self):
        """Test that get_student_mastery method exists with correct signature."""
        db = Mock(spec=Session)
        mastery_engine = MasteryEngine()
        service = MasteryService(db, mastery_engine)
        assert hasattr(service, 'get_student_mastery'), "MasteryService should have get_student_mastery method"
        
        # Check method signature
        sig = inspect.signature(service.get_student_mastery)
        params = list(sig.parameters.keys())
        assert 'student_id' in params, "get_student_mastery should have student_id parameter"
        assert 'concept_id' in params, "get_student_mastery should have concept_id parameter"
    
    def test_update_mastery_method_exists(self):
        """Test that update_mastery method exists with correct signature."""
        db = Mock(spec=Session)
        mastery_engine = MasteryEngine()
        service = MasteryService(db, mastery_engine)
        assert hasattr(service, 'update_mastery'), "MasteryService should have update_mastery method"
        
        # Check method signature
        sig = inspect.signature(service.update_mastery)
        params = list(sig.parameters.keys())
        assert 'student_id' in params, "update_mastery should have student_id parameter"
        assert 'concept_id' in params, "update_mastery should have concept_id parameter"
        assert 'attempt_data' in params, "update_mastery should have attempt_data parameter"
    
    def test_predict_mastery_method_exists(self):
        """Test that predict_mastery method exists with correct signature."""
        db = Mock(spec=Session)
        mastery_engine = MasteryEngine()
        service = MasteryService(db, mastery_engine)
        assert hasattr(service, 'predict_mastery'), "MasteryService should have predict_mastery method"
        
        # Check method signature
        sig = inspect.signature(service.predict_mastery)
        params = list(sig.parameters.keys())
        assert 'student_id' in params, "predict_mastery should have student_id parameter"
        assert 'concept_id' in params, "predict_mastery should have concept_id parameter"
    
    def test_get_weak_concepts_method_exists(self):
        """Test that get_weak_concepts method exists with correct signature."""
        db = Mock(spec=Session)
        mastery_engine = MasteryEngine()
        service = MasteryService(db, mastery_engine)
        assert hasattr(service, 'get_weak_concepts'), "MasteryService should have get_weak_concepts method"
        
        # Check method signature
        sig = inspect.signature(service.get_weak_concepts)
        params = list(sig.parameters.keys())
        assert 'student_id' in params, "get_weak_concepts should have student_id parameter"
        assert 'threshold' in params, "get_weak_concepts should have threshold parameter"
    
    def test_mastery_service_methods_raise_not_implemented(self):
        """Test that MasteryService methods raise NotImplementedError (placeholder)."""
        db = Mock(spec=Session)
        mastery_engine = MasteryEngine()
        service = MasteryService(db, mastery_engine)
        
        with pytest.raises(NotImplementedError):
            service.get_student_mastery(1, 1)
        with pytest.raises(NotImplementedError):
            service.update_mastery(1, 1, {})
        with pytest.raises(NotImplementedError):
            service.predict_mastery(1, 1)
        with pytest.raises(NotImplementedError):
            service.get_weak_concepts(1)



class TestServiceLayerIntegration:
    """Test service layer integration and dependencies."""
    
    def test_all_services_importable(self):
        """Test that all services can be imported without errors."""
        # If we got here, imports at top of file succeeded
        assert True, "All services should be importable"
    
    def test_services_accept_proper_dependencies(self):
        """Test that services properly accept their required dependencies."""
        db = Mock(spec=Session)
        
        # AuthService requires only db
        auth_service = AuthService(db)
        assert auth_service.db is db
        
        # StudentService requires only db
        student_service = StudentService(db)
        assert student_service.db is db
        
        # TeacherService requires only db
        teacher_service = TeacherService(db)
        assert teacher_service.db is db
        
        # ConceptService requires db and ConceptGraph
        concept_graph = ConceptGraph()
        concept_service = ConceptService(db, concept_graph)
        assert concept_service.db is db
        assert concept_service.concept_graph is concept_graph
        
        # AssignmentService requires db, RubricEngine, and optional MasteryService
        rubric_engine = RubricEngine()
        mastery_service = Mock(spec=MasteryService)
        assignment_service = AssignmentService(db, rubric_engine, mastery_service)
        assert assignment_service.db is db
        assert assignment_service.rubric_engine is rubric_engine
        assert assignment_service.mastery_service is mastery_service
        
        # AttemptService requires db and MasteryService
        attempt_service = AttemptService(db, mastery_service)
        assert attempt_service.db is db
        assert attempt_service.mastery_service is mastery_service
        
        # MasteryService requires db and MasteryEngine
        mastery_engine = MasteryEngine()
        mastery_service_real = MasteryService(db, mastery_engine)
        assert mastery_service_real.db is db
        assert mastery_service_real.mastery_engine is mastery_engine
    
    def test_services_are_placeholder_implementations(self):
        """Test that services contain placeholder implementations (raise NotImplementedError)."""
        db = Mock(spec=Session)
        
        # AuthService
        auth_service = AuthService(db)
        with pytest.raises(NotImplementedError):
            auth_service.register_user(Mock())
        with pytest.raises(NotImplementedError):
            auth_service.authenticate_user("test@example.com", "password")
        with pytest.raises(NotImplementedError):
            auth_service.create_access_token(1, "student")
        
        # StudentService
        student_service = StudentService(db)
        with pytest.raises(NotImplementedError):
            student_service.get_student(1)
        with pytest.raises(NotImplementedError):
            student_service.get_student_by_user_id(1)
        
        # TeacherService
        teacher_service = TeacherService(db)
        with pytest.raises(NotImplementedError):
            teacher_service.get_teacher(1)
        with pytest.raises(NotImplementedError):
            teacher_service.get_teacher_by_user_id(1)
        with pytest.raises(NotImplementedError):
            teacher_service.get_class_analytics(1)
        
        # ConceptService
        concept_graph = ConceptGraph()
        concept_service = ConceptService(db, concept_graph)
        with pytest.raises(NotImplementedError):
            concept_service.create_concept(Mock())
        with pytest.raises(NotImplementedError):
            concept_service.get_prerequisites(1)
        with pytest.raises(NotImplementedError):
            concept_service.get_learning_path(1, 1)
        
        # AssignmentService
        rubric_engine = RubricEngine()
        assignment_service = AssignmentService(db, rubric_engine)
        with pytest.raises(NotImplementedError):
            assignment_service.create_assignment(Mock())
        with pytest.raises(NotImplementedError):
            assignment_service.get_assignment(1)
        with pytest.raises(NotImplementedError):
            assignment_service.submit_assignment(1, 1, "content")
        with pytest.raises(NotImplementedError):
            assignment_service.list_assignments()
        
        # AttemptService
        mastery_service = Mock(spec=MasteryService)
        attempt_service = AttemptService(db, mastery_service)
        with pytest.raises(NotImplementedError):
            attempt_service.submit_attempt(Mock())
        with pytest.raises(NotImplementedError):
            attempt_service.get_attempt(1)
        with pytest.raises(NotImplementedError):
            attempt_service.get_student_attempts(1)
        
        # MasteryService
        mastery_engine = MasteryEngine()
        mastery_service_real = MasteryService(db, mastery_engine)
        with pytest.raises(NotImplementedError):
            mastery_service_real.get_student_mastery(1, 1)
        with pytest.raises(NotImplementedError):
            mastery_service_real.update_mastery(1, 1, {})
        with pytest.raises(NotImplementedError):
            mastery_service_real.predict_mastery(1, 1)
        with pytest.raises(NotImplementedError):
            mastery_service_real.get_weak_concepts(1)
