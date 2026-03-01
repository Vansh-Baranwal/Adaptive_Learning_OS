# ALOS Backend

Adaptive Learning OS (ALOS) backend API built with FastAPI.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.template .env
# Edit .env with your database credentials
```

3. Initialize database migrations:
```bash
cd backend
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

## Project Structure

- `app/` - Main application code
  - `api/` - API routes
  - `models/` - SQLAlchemy models
  - `schemas/` - Pydantic schemas
  - `services/` - Business logic layer
  - `ai/` - AI module layer
  - `core/` - Core utilities (security, middleware)
  - `db/` - Database configuration
- `alembic/` - Database migrations
- `tests/` - Test suite

## Database Migration Commands

Generate migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```
