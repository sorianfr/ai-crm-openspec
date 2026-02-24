## ADDED Requirements

### Requirement: FastAPI application structure

The system SHALL provide a well-organized FastAPI project structure with proper module separation, following Python best practices.

#### Scenario: Application entry point exists
- **WHEN** the application starts
- **THEN** a main entry point file SHALL exist at `app/main.py`
- **AND** it SHALL create and configure a FastAPI application instance

#### Scenario: Project organization
- **WHEN** examining the project structure
- **THEN** the project SHALL have the following structure:
  - `app/main.py`: Application entry point
  - `app/core/config.py`: Configuration module
  - `app/db/session.py`: Database session management
  - `app/db/base.py`: Database base configuration
  - `app/routes/`: Route handlers directory
  - `app/templates/`: Jinja2 templates directory
  - `app/static/`: Static assets directory
- **AND** modules SHALL be organized by functionality

#### Scenario: FastAPI app configuration
- **WHEN** the FastAPI application is initialized
- **THEN** it SHALL be configured with appropriate metadata (title, description, version)
- **AND** it SHALL enable automatic OpenAPI documentation at `/docs` and `/redoc`

### Requirement: Configuration from environment (12-factor)

The application SHALL read configuration from environment variables. The config module (e.g. `app/core/config.py`) SHALL load at least: `DATABASE_URL` (database connection string), `DEBUG` (boolean), and `APP_ENV` (e.g. development, staging, production). Defaults when env vars are unset SHALL be production-safe where applicable (e.g. DEBUG defaults to false). When `APP_ENV` indicates production, the application SHALL require `DATABASE_URL` to be set (e.g. fail fast at startup if missing); when not production, a default database URL MAY be used for development.

#### Scenario: Config loaded from environment
- **WHEN** the application starts
- **THEN** the config module SHALL read `DATABASE_URL`, `DEBUG`, and `APP_ENV` from the environment
- **AND** `DEBUG` SHALL default to false when unset
- **AND** `APP_ENV` SHALL have a default (e.g. development) when unset

#### Scenario: Production requires DATABASE_URL
- **WHEN** `APP_ENV` is set to a production value (e.g. production) and `DATABASE_URL` is not set
- **THEN** the application SHALL fail fast at startup (e.g. raise or exit) rather than using a default database URL

#### Scenario: Non-production may use default database
- **WHEN** `APP_ENV` is not production and `DATABASE_URL` is not set
- **THEN** the application MAY use a default database URL (e.g. SQLite for development) and SHALL start successfully

### Requirement: Run contract for container deployment

The standard way to run the application with uvicorn SHALL bind the server to `0.0.0.0` so the app is reachable from outside the host (e.g. in containers). This SHALL be achieved via the run contract (e.g. `uvicorn app.main:app --host 0.0.0.0` in scripts, pyproject.toml, or documented run instructions).

#### Scenario: Uvicorn binds to 0.0.0.0
- **WHEN** the application is run via the standard run contract (e.g. documented command or project script)
- **THEN** uvicorn SHALL be invoked with `--host 0.0.0.0` (or equivalent) so the server accepts connections from any interface
- **AND** the app SHALL be deployable in containers without code changes to the bind address

### Requirement: Container entrypoint startup flow

When the application is run in a container, the entrypoint SHALL orchestrate startup so that the database is ready, migrations are applied, and then the application server is started.

#### Scenario: Entrypoint waits for database
- **WHEN** the container entrypoint runs
- **THEN** it SHALL wait for the database to be ready (e.g. pg_isready loop or depends_on with healthcheck) before running migrations or starting the app
- **AND** SHALL exit or retry on failure until the database is available (within a reasonable limit)

#### Scenario: Entrypoint runs migrations then server
- **WHEN** the database is ready
- **THEN** the entrypoint SHALL run `alembic upgrade head`
- **AND** SHALL then start the application server (e.g. uvicorn app.main:app --host 0.0.0.0 --port 8000)
- **AND** SHALL NOT start the server if migrations fail

#### Scenario: Entrypoint script location
- **WHEN** the container is built
- **THEN** an entrypoint script (e.g. docker/entrypoint.sh) SHALL be copied into the image and invoked as the container ENTRYPOINT or CMD
- **AND** the script SHALL be executable and suitable for the runtime user (e.g. non-root)
