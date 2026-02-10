## Context

This is a greenfield project bootstrap. We're establishing the technical foundation for a Python web application that will eventually support CRM functionality. The goal is to create a minimal, well-structured foundation using modern Python web technologies: FastAPI for the web framework, SQLite for the database, SQLAlchemy for ORM, Alembic for migrations, Jinja2 for templating, and HTMX for client-side interactions.

The foundation must be simple enough to get started quickly, but structured enough to scale as domain features are added. No existing codebase or infrastructure exists - this is a fresh start.

## Goals / Non-Goals

**Goals:**
- Establish a clean, maintainable project structure following Python best practices
- Configure all core technical components (FastAPI, database, migrations, templating)
- Provide basic endpoints (health check, homepage) to verify the stack works
- Enable rapid development of domain features without infrastructure changes
- Keep dependencies minimal and well-documented

**Non-Goals:**
- Domain-specific CRM features (customers, contacts, etc.)
- Authentication or authorization
- Complex business logic
- Production deployment configuration (Docker, CI/CD, etc.)
- Testing infrastructure (though structure should support it)

## Decisions

### Decision 1: Project Structure

**Approach**: Use an `app/` package with clear separation of concerns:
```
project/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── core/
│   │   └── config.py        # Configuration management
│   ├── db/
│   │   ├── session.py       # Database session management
│   │   └── base.py         # Database base configuration
│   ├── routes/
│   │   ├── health.py       # Health endpoint
│   │   └── home.py         # Homepage route
│   ├── templates/
│   │   ├── base.html       # Base template (HTMX via CDN)
│   │   └── index.html      # Homepage template
│   └── static/             # Static assets
├── alembic.ini             # Alembic configuration
├── alembic/                # Migration files
├── requirements.txt
├── .env.example
└── README.md
```

**Rationale**: Package structure under `app/` keeps application code organized and matches the concrete paths required by the specs.

**Alternatives considered**:
- Package-based structure (`src/` directory): More complex for initial bootstrap, better for larger projects
- Monolithic single file: Too limiting, doesn't scale

### Decision 2: Database Configuration

**Approach**: Use environment variables for database path, with a default fallback. SQLite file will be created in the project root or a `data/` directory.

**Rationale**: Environment-based configuration allows flexibility for different environments (dev, test, prod) without code changes. SQLite file location should be configurable but have sensible defaults.

**Alternatives considered**:
- Hardcoded database path: Not flexible, harder to test
- Separate config files: More complex than needed for initial bootstrap

### Decision 3: Alembic Integration

**Approach**: Configure Alembic to use the same database connection as the application, using SQLAlchemy's connection string from the application config.

**Rationale**: Ensures migrations run against the same database configuration as the application. This prevents configuration drift and makes migrations reliable.

**Alternatives considered**:
- Manual schema management: Error-prone, doesn't scale
- Separate Alembic config: More complex, potential for misconfiguration

### Decision 4: Template Organization

**Approach**: Use a base template at `app/templates/base.html` that other templates extend. Include HTMX via CDN script tag in the base template.

**Rationale**: Base template provides consistent structure (HTML head, navigation, footer). CDN link for HTMX avoids managing library versions and updates. Can switch to static file later if needed.

**Alternatives considered**:
- Static HTMX file: More control but requires version management
- No base template: Code duplication, harder to maintain consistency

### Decision 5: Health Endpoint Implementation

**Approach**: Simple JSON response with status indicator. No database checks initially (can add later if needed).

**Rationale**: Minimal implementation meets the requirement. Can extend later to check database connectivity, external services, etc. Keep it simple for bootstrap.

**Alternatives considered**:
- Comprehensive health checks: Overkill for initial bootstrap
- HTML response: Less useful for monitoring tools that expect JSON

## Risks / Trade-offs

**Risk**: SQLite may not scale for production workloads
- **Mitigation**: This is acceptable for bootstrap. Migration to PostgreSQL/MySQL can be done later by changing the connection string and running migrations.

**Risk**: Flat project structure may need refactoring as project grows
- **Mitigation**: Structure is intentionally simple. Refactoring into packages is straightforward when needed.

**Risk**: HTMX via CDN requires internet connectivity
- **Mitigation**: Acceptable for development. Can switch to static file for offline development or production if needed.

**Trade-off**: Minimal configuration vs. flexibility
- **Decision**: Start minimal, add configuration as needed. Environment variables provide enough flexibility for initial needs.

**Trade-off**: Simple health endpoint vs. comprehensive monitoring
- **Decision**: Start simple. Can add database checks, dependency checks, etc. later without breaking changes.

## Migration Plan

**Initial Setup Steps:**
1. Create project structure and files
2. Install dependencies from `requirements.txt`
3. Copy `.env.example` to `.env` and configure database path
4. Run `alembic upgrade head` to initialize database
5. Start application with `uvicorn app:app --reload`
6. Verify health endpoint at `http://localhost:8000/health`
7. Verify homepage at `http://localhost:8000/`

**Rollback**: Since this is a new project, rollback is simply not deploying or removing the codebase. No data migration needed.

## Open Questions

- Should we include a basic `.gitignore` file? (Yes, for Python projects)
- Should we include a basic logging configuration? (Defer to later - use FastAPI defaults initially)
- Should the database file be gitignored? (Yes, database files should not be committed)
