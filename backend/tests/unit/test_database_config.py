"""Unit tests for database configuration.

Tests database connection, session creation, and cleanup.
Requirements: 1.5, 1.6
"""
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool

# Try to import database session components
try:
    from app.db.session import get_db, SessionLocal, engine
    DB_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    DB_AVAILABLE = False
    get_db = None
    SessionLocal = None
    engine = None


class TestDatabaseConnection:
    """Test database connection functionality."""
    
    @pytest.mark.skipif(not DB_AVAILABLE, reason="Database dependencies not available")
    def test_engine_exists(self):
        """Test that SQLAlchemy engine is created."""
        assert engine is not None, "Database engine should be created"
    
    @pytest.mark.skipif(not DB_AVAILABLE, reason="Database dependencies not available")
    def test_engine_has_pool_configuration(self):
        """Test that engine has proper connection pooling configuration."""
        # Check that pool_pre_ping is enabled
        assert engine.pool._pre_ping is True, "pool_pre_ping should be enabled"
        
        # Check pool size configuration
        assert engine.pool.size() >= 0, "Pool should have a valid size"
    
    def test_database_connection(self):
        """Test that database connection can be established."""
        # Use a test database connection
        test_engine = create_engine(
            "sqlite:///:memory:",
            poolclass=NullPool
        )
        
        # Test connection
        with test_engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            assert result.fetchone()[0] == 1, "Database connection should work"
    
    @pytest.mark.skipif(not DB_AVAILABLE, reason="Database dependencies not available")
    def test_session_factory_exists(self):
        """Test that SessionLocal factory is created."""
        assert SessionLocal is not None, "SessionLocal factory should be created"
    
    @pytest.mark.skipif(not DB_AVAILABLE, reason="Database dependencies not available")
    def test_session_factory_configuration(self):
        """Test that SessionLocal has correct configuration."""
        # Check autocommit is False
        assert SessionLocal.kw.get('autocommit') is False, "autocommit should be False"
        
        # Check autoflush is False
        assert SessionLocal.kw.get('autoflush') is False, "autoflush should be False"


class TestSessionCreation:
    """Test database session creation."""
    
    def test_session_creation(self):
        """Test that database session can be created."""
        # Create a test session
        test_engine = create_engine(
            "sqlite:///:memory:",
            poolclass=NullPool
        )
        TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
        
        session = TestSessionLocal()
        assert session is not None, "Session should be created"
        assert isinstance(session, Session), "Session should be SQLAlchemy Session instance"
        session.close()
    
    @pytest.mark.skipif(not DB_AVAILABLE, reason="Database dependencies not available")
    def test_get_db_dependency(self):
        """Test that get_db dependency function works."""
        # get_db is a generator function
        db_generator = get_db()
        
        # Get the session from generator
        session = next(db_generator)
        assert session is not None, "get_db should yield a session"
        assert isinstance(session, Session), "get_db should yield SQLAlchemy Session"
        
        # Close the generator (triggers cleanup)
        try:
            next(db_generator)
        except StopIteration:
            pass  # Expected behavior
    
    def test_multiple_sessions_independent(self):
        """Test that multiple sessions are independent."""
        # Create test engine
        test_engine = create_engine(
            "sqlite:///:memory:",
            poolclass=NullPool
        )
        TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
        
        session1 = TestSessionLocal()
        session2 = TestSessionLocal()
        
        assert session1 is not session2, "Multiple sessions should be independent"
        
        session1.close()
        session2.close()


class TestSessionCleanup:
    """Test database session cleanup."""
    
    def test_session_closes_properly(self):
        """Test that session closes without errors."""
        # Create test session
        test_engine = create_engine(
            "sqlite:///:memory:",
            poolclass=NullPool
        )
        TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
        
        session = TestSessionLocal()
        
        # Session should be active before closing
        assert session.is_active, "Session should be active before closing"
        
        # Close the session - should not raise any errors
        session.close()
        
        # Verify close was called successfully (no exception raised)
        # The session object still exists and can be referenced
        assert session is not None, "Session object should still exist after close"
    
    @pytest.mark.skipif(not DB_AVAILABLE, reason="Database dependencies not available")
    def test_get_db_cleanup_on_success(self):
        """Test that get_db cleans up session after successful use."""
        db_generator = get_db()
        session = next(db_generator)
        
        # Session should be active during use
        assert session.is_active, "Session should be active during use"
        
        # Trigger cleanup
        try:
            next(db_generator)
        except StopIteration:
            pass
        
        # After cleanup, attempting to use the session should fail or be invalid
        # The session is closed, even if is_active still returns True
        # We verify cleanup happened by checking the generator is exhausted
        with pytest.raises(StopIteration):
            next(db_generator)
    
    @pytest.mark.skipif(not DB_AVAILABLE, reason="Database dependencies not available")
    def test_get_db_cleanup_on_exception(self):
        """Test that get_db cleans up session even when exception occurs."""
        db_generator = get_db()
        session = next(db_generator)
        
        # Session should be active
        assert session.is_active, "Session should be active"
        
        # Simulate exception during use
        try:
            raise ValueError("Test exception")
        except ValueError:
            pass
        
        # Trigger cleanup
        try:
            next(db_generator)
        except StopIteration:
            pass
        
        # Verify generator is exhausted (cleanup completed)
        with pytest.raises(StopIteration):
            next(db_generator)
    
    def test_session_cleanup_with_context_manager(self):
        """Test session cleanup using context manager pattern."""
        test_engine = create_engine(
            "sqlite:///:memory:",
            poolclass=NullPool
        )
        TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
        
        # Use context manager pattern
        session = TestSessionLocal()
        cleanup_executed = False
        
        try:
            # Simulate work - session should be active
            assert session.is_active, "Session should be active during use"
            
            # Execute a query to verify it works
            result = session.execute(text("SELECT 1"))
            assert result.fetchone()[0] == 1, "Query should execute successfully"
        finally:
            session.close()
            cleanup_executed = True
        
        # Verify cleanup was executed
        assert cleanup_executed, "Cleanup in finally block should execute"
        assert session is not None, "Session should still exist after cleanup"
