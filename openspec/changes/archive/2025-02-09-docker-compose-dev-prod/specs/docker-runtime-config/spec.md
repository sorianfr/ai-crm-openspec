# Docker runtime configuration

The system SHALL provide reproducible Docker Compose configurations for development and production, with required environment variables, distinct dev/prod behavior, and an app entrypoint that runs migrations before starting the server.

## Requirements

### Requirement: Required environment variables

The Docker runtime SHALL expect the following environment variables for the application container: `DATABASE_URL`, `JWT_SECRET`, `SESSION_SECRET`, `APP_ENV`, `DEBUG`, and `JWT_EXPIRATION_MINUTES`. Production SHALL require `JWT_SECRET` and `SESSION_SECRET` to be set (non-empty); development MAY use safe default values.

#### Scenario: Required vars documented
- **WHEN** deploying the application in Docker
- **THEN** the set of required env vars SHALL be documented (e.g. in .env.prod.example or README)
- **AND** production SHALL fail fast or refuse to start if JWT_SECRET or SESSION_SECRET are missing or empty

#### Scenario: DATABASE_URL consistency
- **WHEN** the application and Alembic run in Docker
- **THEN** both SHALL use the same `DATABASE_URL` from the environment (e.g. postgresql+psycopg for psycopg v3)
- **AND** the driver in DATABASE_URL SHALL match the installed database driver

### Requirement: Development vs production behavior

The system SHALL provide separate Compose configurations for development and production.

#### Scenario: Development configuration
- **WHEN** running with the development Compose configuration
- **THEN** `APP_ENV` SHALL be development (or equivalent)
- **AND** Secure cookie SHALL be disabled so sessions work over http://localhost
- **AND** the app port (e.g. 8000) and the Postgres port (e.g. 5432) SHALL be exposed to the host

#### Scenario: Production configuration
- **WHEN** running with the production Compose configuration
- **THEN** `APP_ENV` SHALL be production (or equivalent)
- **AND** Secure cookie SHALL be enabled (assuming HTTPS at reverse proxy)
- **AND** the Postgres port SHALL NOT be published to the host (no host mapping for 5432)

### Requirement: Entrypoint runs migrations on start

The application container entrypoint SHALL run database migrations before starting the application server so that missing-table startup failures are prevented.

#### Scenario: Migrations run before app start
- **WHEN** the application container starts
- **THEN** the entrypoint SHALL wait for the database to be ready (e.g. pg_isready or healthcheck)
- **AND** SHALL run `alembic upgrade head` before starting the application process (e.g. uvicorn)
- **AND** SHALL start the application only after migrations complete successfully

#### Scenario: Same DATABASE_URL for migrations and app
- **WHEN** the entrypoint runs Alembic and then starts the app
- **THEN** both SHALL use the same `DATABASE_URL` from the environment

### Requirement: bcrypt compatibility in container

The system SHALL pin the bcrypt dependency to a version compatible with passlib in the container runtime (e.g. bcrypt<4) to avoid runtime failures.

#### Scenario: bcrypt pin in requirements
- **WHEN** building the application Docker image
- **THEN** requirements SHALL include a pin that ensures bcrypt compatibility with passlib (e.g. bcrypt<4)
- **AND** password hashing (login, user creation) SHALL work correctly inside the container
