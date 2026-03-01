"""Unit tests for project structure validation.

Tests that all required directories exist and configuration files are present and valid.
Requirements: 5.1, 5.5, 5.6, 6.1
"""
import os
import pytest
from pathlib import Path


# Get the backend directory path
BACKEND_DIR = Path(__file__).parent.parent.parent
# Get the project root directory (parent of backend)
PROJECT_ROOT = BACKEND_DIR.parent


class TestDirectoryStructure:
    """Test that all required directories exist."""
    
    def test_app_directory_exists(self):
        """Test that the main app directory exists."""
        app_dir = BACKEND_DIR / "app"
        assert app_dir.exists(), "app/ directory should exist"
        assert app_dir.is_dir(), "app/ should be a directory"
    
    def test_api_directories_exist(self):
        """Test that API layer directories exist."""
        api_dir = BACKEND_DIR / "app" / "api"
        assert api_dir.exists(), "app/api/ directory should exist"
        
        api_v1_dir = api_dir / "v1"
        assert api_v1_dir.exists(), "app/api/v1/ directory should exist"
    
    def test_services_directory_exists(self):
        """Test that services directory exists."""
        services_dir = BACKEND_DIR / "app" / "services"
        assert services_dir.exists(), "app/services/ directory should exist"
        assert services_dir.is_dir(), "app/services/ should be a directory"
    
    def test_ai_directory_exists(self):
        """Test that AI module directory exists."""
        ai_dir = BACKEND_DIR / "app" / "ai"
        assert ai_dir.exists(), "app/ai/ directory should exist"
        assert ai_dir.is_dir(), "app/ai/ should be a directory"
    
    def test_models_directory_exists(self):
        """Test that models directory exists."""
        models_dir = BACKEND_DIR / "app" / "models"
        assert models_dir.exists(), "app/models/ directory should exist"
        assert models_dir.is_dir(), "app/models/ should be a directory"
    
    def test_schemas_directory_exists(self):
        """Test that schemas directory exists."""
        schemas_dir = BACKEND_DIR / "app" / "schemas"
        assert schemas_dir.exists(), "app/schemas/ directory should exist"
        assert schemas_dir.is_dir(), "app/schemas/ should be a directory"
    
    def test_core_directory_exists(self):
        """Test that core utilities directory exists."""
        core_dir = BACKEND_DIR / "app" / "core"
        assert core_dir.exists(), "app/core/ directory should exist"
        assert core_dir.is_dir(), "app/core/ should be a directory"
    
    def test_db_directory_exists(self):
        """Test that database configuration directory exists."""
        db_dir = BACKEND_DIR / "app" / "db"
        assert db_dir.exists(), "app/db/ directory should exist"
        assert db_dir.is_dir(), "app/db/ should be a directory"
    
    def test_alembic_directory_exists(self):
        """Test that Alembic migrations directory exists."""
        alembic_dir = BACKEND_DIR / "alembic"
        assert alembic_dir.exists(), "alembic/ directory should exist"
        assert alembic_dir.is_dir(), "alembic/ should be a directory"
        
        versions_dir = alembic_dir / "versions"
        assert versions_dir.exists(), "alembic/versions/ directory should exist"
    
    def test_tests_directory_exists(self):
        """Test that tests directory exists."""
        tests_dir = BACKEND_DIR / "tests"
        assert tests_dir.exists(), "tests/ directory should exist"
        assert tests_dir.is_dir(), "tests/ should be a directory"
        
        unit_tests_dir = tests_dir / "unit"
        assert unit_tests_dir.exists(), "tests/unit/ directory should exist"


class TestConfigurationFiles:
    """Test that configuration files are present and valid."""
    
    def test_requirements_txt_exists(self):
        """Test that requirements.txt exists."""
        requirements_file = BACKEND_DIR / "requirements.txt"
        assert requirements_file.exists(), "requirements.txt should exist"
        assert requirements_file.is_file(), "requirements.txt should be a file"
    
    def test_requirements_txt_valid(self):
        """Test that requirements.txt contains required dependencies."""
        requirements_file = BACKEND_DIR / "requirements.txt"
        content = requirements_file.read_text()
        
        required_packages = [
            "fastapi",
            "uvicorn",
            "sqlalchemy",
            "alembic",
            "psycopg2-binary",
            "pydantic",
            "python-jose",
            "passlib",
            "python-multipart",
            "pytest",
            "hypothesis"
        ]
        
        for package in required_packages:
            assert package in content.lower(), f"{package} should be in requirements.txt"
    
    def test_env_template_exists(self):
        """Test that .env.template exists."""
        env_template = BACKEND_DIR / ".env.template"
        assert env_template.exists(), ".env.template should exist"
        assert env_template.is_file(), ".env.template should be a file"
    
    def test_env_template_valid(self):
        """Test that .env.template contains required environment variables."""
        env_template = BACKEND_DIR / ".env.template"
        content = env_template.read_text()
        
        required_vars = [
            "DATABASE_URL",
            "SECRET_KEY",
            "ALGORITHM",
            "ACCESS_TOKEN_EXPIRE_MINUTES",
            "ALLOWED_ORIGINS",
            "ENVIRONMENT"
        ]
        
        for var in required_vars:
            assert var in content, f"{var} should be in .env.template"
    
    def test_dockerfile_exists(self):
        """Test that Dockerfile exists."""
        dockerfile = BACKEND_DIR / "Dockerfile"
        assert dockerfile.exists(), "Dockerfile should exist"
        assert dockerfile.is_file(), "Dockerfile should be a file"
    
    def test_dockerfile_valid(self):
        """Test that Dockerfile contains essential commands."""
        dockerfile = BACKEND_DIR / "Dockerfile"
        content = dockerfile.read_text()
        
        # Check for essential Dockerfile commands
        assert "FROM" in content, "Dockerfile should have FROM instruction"
        assert "WORKDIR" in content, "Dockerfile should have WORKDIR instruction"
        assert "COPY" in content or "ADD" in content, "Dockerfile should copy files"
        assert "RUN" in content or "CMD" in content, "Dockerfile should have execution commands"
    
    def test_alembic_ini_exists(self):
        """Test that alembic.ini exists."""
        alembic_ini = BACKEND_DIR / "alembic.ini"
        assert alembic_ini.exists(), "alembic.ini should exist"
        assert alembic_ini.is_file(), "alembic.ini should be a file"
    
    def test_alembic_ini_valid(self):
        """Test that alembic.ini contains required configuration."""
        alembic_ini = BACKEND_DIR / "alembic.ini"
        content = alembic_ini.read_text()
        
        # Check for essential Alembic configuration
        assert "[alembic]" in content, "alembic.ini should have [alembic] section"
        assert "script_location" in content, "alembic.ini should specify script_location"
        assert "sqlalchemy.url" in content, "alembic.ini should specify sqlalchemy.url"


class TestModuleFiles:
    """Test that essential module files exist."""
    
    def test_main_py_exists(self):
        """Test that main.py exists."""
        main_file = BACKEND_DIR / "app" / "main.py"
        assert main_file.exists(), "app/main.py should exist"
        assert main_file.is_file(), "app/main.py should be a file"
    
    def test_init_files_exist(self):
        """Test that __init__.py files exist in all packages."""
        required_init_files = [
            BACKEND_DIR / "app" / "__init__.py",
            BACKEND_DIR / "app" / "api" / "__init__.py",
            BACKEND_DIR / "app" / "api" / "v1" / "__init__.py",
            BACKEND_DIR / "app" / "services" / "__init__.py",
            BACKEND_DIR / "app" / "ai" / "__init__.py",
            BACKEND_DIR / "app" / "models" / "__init__.py",
            BACKEND_DIR / "app" / "schemas" / "__init__.py",
            BACKEND_DIR / "app" / "core" / "__init__.py",
            BACKEND_DIR / "app" / "db" / "__init__.py",
            BACKEND_DIR / "tests" / "__init__.py",
            BACKEND_DIR / "tests" / "unit" / "__init__.py"
        ]
        
        for init_file in required_init_files:
            assert init_file.exists(), f"{init_file.relative_to(BACKEND_DIR)} should exist"
    
    def test_core_modules_exist(self):
        """Test that core module files exist."""
        security_file = BACKEND_DIR / "app" / "core" / "security.py"
        assert security_file.exists(), "app/core/security.py should exist"
        
        middleware_file = BACKEND_DIR / "app" / "core" / "middleware.py"
        assert middleware_file.exists(), "app/core/middleware.py should exist"
    
    def test_db_modules_exist(self):
        """Test that database module files exist."""
        session_file = BACKEND_DIR / "app" / "db" / "session.py"
        assert session_file.exists(), "app/db/session.py should exist"
        
        base_file = BACKEND_DIR / "app" / "db" / "base.py"
        assert base_file.exists(), "app/db/base.py should exist"
    
    def test_ai_modules_exist(self):
        """Test that AI module files exist."""
        ai_modules = [
            "mastery_engine.py",
            "readiness.py",
            "concept_graph.py",
            "rubric_engine.py"
        ]
        
        for module in ai_modules:
            module_file = BACKEND_DIR / "app" / "ai" / module
            assert module_file.exists(), f"app/ai/{module} should exist"
    
    def test_model_files_exist(self):
        """Test that model files exist."""
        model_files = [
            "base.py",
            "user.py",
            "student.py",
            "teacher.py",
            "concept.py",
            "assignment.py",
            "attempt.py",
            "mastery.py"
        ]
        
        for model_file in model_files:
            file_path = BACKEND_DIR / "app" / "models" / model_file
            assert file_path.exists(), f"app/models/{model_file} should exist"
    
    def test_schema_files_exist(self):
        """Test that schema files exist."""
        schema_files = [
            "user.py",
            "student.py",
            "teacher.py",
            "concept.py",
            "assignment.py",
            "attempt.py",
            "mastery.py"
        ]
        
        for schema_file in schema_files:
            file_path = BACKEND_DIR / "app" / "schemas" / schema_file
            assert file_path.exists(), f"app/schemas/{schema_file} should exist"
    
    def test_service_files_exist(self):
        """Test that service files exist."""
        service_files = [
            "auth_service.py",
            "student_service.py",
            "teacher_service.py",
            "concept_service.py",
            "assignment_service.py",
            "attempt_service.py",
            "mastery_service.py"
        ]
        
        for service_file in service_files:
            file_path = BACKEND_DIR / "app" / "services" / service_file
            assert file_path.exists(), f"app/services/{service_file} should exist"


class TestFrontendScopeLimitation:
    """Test that frontend directory contains no implementation.
    
    Requirements: 6.1
    """
    
    def test_frontend_directory_exists(self):
        """Test that frontend directory exists as a placeholder."""
        frontend_dir = PROJECT_ROOT / "frontend"
        assert frontend_dir.exists(), "frontend/ directory should exist"
        assert frontend_dir.is_dir(), "frontend/ should be a directory"
    
    def test_frontend_contains_no_implementation(self):
        """Test that frontend directory contains no implementation files.
        
        The frontend directory should only contain a README.md placeholder
        and no actual implementation files (no .js, .jsx, .ts, .tsx, .vue, etc.).
        
        Requirements: 6.1
        """
        frontend_dir = PROJECT_ROOT / "frontend"
        
        # Implementation file extensions that should NOT be present
        implementation_extensions = {
            '.js', '.jsx', '.ts', '.tsx',  # JavaScript/TypeScript
            '.vue', '.svelte',              # Vue/Svelte
            '.html', '.css', '.scss',       # HTML/CSS
            '.json',                        # Config files (package.json, tsconfig.json, etc.)
        }
        
        # Get all files in frontend directory (recursively)
        all_files = []
        if frontend_dir.exists():
            for item in frontend_dir.rglob('*'):
                if item.is_file():
                    all_files.append(item)
        
        # Check that no implementation files exist
        implementation_files = [
            f for f in all_files 
            if f.suffix.lower() in implementation_extensions
        ]
        
        assert len(implementation_files) == 0, (
            f"Frontend directory should contain no implementation files. "
            f"Found: {[str(f.relative_to(frontend_dir)) for f in implementation_files]}"
        )
    
    def test_frontend_contains_only_readme(self):
        """Test that frontend directory contains only README.md.
        
        Requirements: 6.1
        """
        frontend_dir = PROJECT_ROOT / "frontend"
        
        # Get all files in frontend directory (non-recursive, just top level)
        files_in_frontend = [
            f for f in frontend_dir.iterdir() 
            if f.is_file()
        ]
        
        # Should only contain README.md
        assert len(files_in_frontend) == 1, (
            f"Frontend directory should contain only README.md. "
            f"Found: {[f.name for f in files_in_frontend]}"
        )
        
        assert files_in_frontend[0].name == "README.md", (
            "The only file in frontend directory should be README.md"
        )
    
    def test_frontend_readme_indicates_not_implemented(self):
        """Test that frontend README.md indicates frontend is not implemented.
        
        Requirements: 6.1
        """
        frontend_readme = PROJECT_ROOT / "frontend" / "README.md"
        
        assert frontend_readme.exists(), "frontend/README.md should exist"
        
        content = frontend_readme.read_text().lower()
        
        # Check that README indicates frontend is not implemented
        not_implemented_indicators = [
            "not implemented",
            "placeholder",
            "out of scope",
            "not included"
        ]
        
        has_indicator = any(indicator in content for indicator in not_implemented_indicators)
        
        assert has_indicator, (
            "frontend/README.md should indicate that frontend is not implemented"
        )
