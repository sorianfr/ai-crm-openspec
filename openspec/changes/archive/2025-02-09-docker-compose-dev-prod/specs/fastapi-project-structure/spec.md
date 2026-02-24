## ADDED Requirements

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
