## 1. Project Structure Setup

- [x] 1.1 Create `app/` package and directory structure (app/core/, app/db/, app/routes/, app/templates/, app/static/)
- [x] 1.2 Create `requirements.txt` with all dependencies (FastAPI, SQLAlchemy, Alembic, Jinja2, python-dotenv, uvicorn)
- [x] 1.3 Create `.env.example` file with example environment variables (database path, debug mode)
- [x] 1.4 Create `.gitignore` file for Python projects (include database files, __pycache__, .env)
- [x] 1.5 Create `README.md` with project description and setup instructions

## 2. Configuration Module

- [x] 2.1 Create `app/core/config.py` module for application configuration
- [x] 2.2 Implement environment variable loading using python-dotenv
- [x] 2.3 Add database path configuration with default fallback
- [x] 2.4 Add debug mode configuration

## 3. Database Setup

- [x] 3.1 Create `app/db/base.py` for database base configuration
- [x] 3.2 Create `app/db/session.py` for database connection and session management
- [x] 3.3 Configure SQLAlchemy engine with SQLite connection string (DB file created on first connection)
- [x] 3.4 Create SQLAlchemy session factory and dependency for FastAPI route handlers
- [x] 3.5 Add database connection lifecycle management (create/close sessions)

## 4. Alembic Migrations

- [x] 4.1 Initialize Alembic in the project (`alembic init alembic`)
- [x] 4.2 Configure `alembic.ini` and `alembic/env.py` to use application's database connection
- [x] 4.3 Update Alembic env.py to use SQLAlchemy metadata from app.db
- [x] 4.4 Optionally create initial migration (`alembic revision --autogenerate -m "Initial migration"`)

## 5. FastAPI Application Setup

- [x] 5.1 Create `app/main.py` as FastAPI application entry point
- [x] 5.2 Initialize FastAPI app with metadata (title, description, version)
- [x] 5.3 Configure automatic OpenAPI documentation at `/docs` and `/redoc`
- [x] 5.4 Set up application startup and shutdown event handlers

## 6. Jinja2 Template Integration

- [x] 6.1 Configure Jinja2Templates in FastAPI application
- [x] 6.2 Set template directory path to `app/templates/`
- [x] 6.3 Create `app/templates/base.html` base template with HTML structure
- [x] 6.4 Include HTMX library in base template via CDN script tag
- [x] 6.5 Create `app/templates/index.html` homepage template extending base template

## 7. Static Files Setup

- [x] 7.1 Configure FastAPI to serve static files from `app/static/` directory
- [x] 7.2 Mount static file route in FastAPI application

## 8. Health Endpoint

- [x] 8.1 Create `app/routes/health.py` with GET `/health` endpoint
- [x] 8.2 Implement endpoint returning JSON `{"status": "ok"}`
- [x] 8.3 Register health router in `app/main.py`

## 9. Homepage Route

- [x] 9.1 Create `app/routes/home.py` with GET `/` route
- [x] 9.2 Implement route rendering `app/templates/index.html` template
- [x] 9.3 Register homepage router in `app/main.py`

## 10. Verification

- [x] 10.1 Verify application starts without errors (e.g. `uvicorn app.main:app --reload`)
- [x] 10.2 Verify health endpoint returns correct response at `/health`
- [x] 10.3 Verify homepage loads correctly at `/`
- [x] 10.4 Verify OpenAPI documentation is accessible at `/docs`
- [x] 10.5 Verify database file is created when connection is first opened or migrations applied
- [x] 10.6 Verify Alembic migrations can be run successfully
