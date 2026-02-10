## Why

We need to establish the technical foundation for a Python web application. This bootstrap change creates the essential infrastructure: FastAPI project structure, SQLite database setup with SQLAlchemy and Alembic migrations, Jinja2 templating, HTMX integration, and basic endpoints. This foundation will enable future development of domain-specific features without requiring changes to the core technical stack.

## What Changes

- **New project structure**: Create a minimal Python web application scaffold with FastAPI
- **FastAPI application**: Basic FastAPI app with proper project organization
- **SQLite + SQLAlchemy setup**: Database connection, session management, and base configuration
- **Alembic migrations**: Database migration system configured and initialized
- **Jinja2 templating**: Template engine configured for server-side HTML rendering
- **HTMX integration**: HTMX library included (via CDN or static file) for future interactive features
- **Health endpoint**: Basic `/health` API endpoint for monitoring and readiness checks
- **Homepage**: Simple homepage route serving a basic HTML template
- **Project setup**: Requirements file, project structure, configuration, and basic documentation

## Capabilities

### New Capabilities
- `fastapi-project-structure`: Organized FastAPI application structure with proper module separation
- `database-setup`: SQLite database connection and SQLAlchemy session management
- `alembic-migrations`: Alembic configuration and migration infrastructure
- `jinja2-templating`: Jinja2 template engine integration with FastAPI
- `htmx-integration`: HTMX library setup for future dynamic web interactions
- `health-endpoint`: Basic health check API endpoint
- `homepage`: Simple homepage route and template

### Modified Capabilities
<!-- No existing capabilities to modify - this is a new project bootstrap -->

## Impact

- **New files**: Minimal project structure including:
  - `main.py` or `app.py`: FastAPI application entry point
  - `database.py`: Database connection and session management
  - `alembic.ini`: Alembic configuration file
  - `alembic/`: Alembic migration directory with initial migration
  - `templates/`: Jinja2 HTML templates directory (with base template and homepage)
  - `static/`: Static assets directory (HTMX library)
  - `requirements.txt`: Python dependencies
  - `README.md`: Project documentation
  - `.env.example`: Example environment configuration
- **Dependencies**: FastAPI, SQLAlchemy, Alembic, Jinja2, HTMX (via CDN or static file), python-dotenv, uvicorn
- **Database**: SQLite database file will be created on first run (name configurable)
- **Configuration**: Environment-based configuration for database path, debug mode, etc.
