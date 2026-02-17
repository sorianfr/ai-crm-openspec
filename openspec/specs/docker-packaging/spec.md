# Docker packaging

The project provides a Docker image for the FastAPI CRM so the app can run in containers using 12-factor configuration.

## Requirements

### Requirement: Dockerfile

The project SHALL provide a Dockerfile that builds a runnable image of the application. The image SHALL be based on `python:3.11-slim`. The image SHALL install application dependencies from requirements.txt and copy the application code. The container SHALL run the FastAPI app via uvicorn bound to `0.0.0.0:8000`. The process inside the container SHALL run as a non-root user.

#### Scenario: Image builds successfully
- **WHEN** the user runs `docker build` from the project root with the project's Dockerfile
- **THEN** the build SHALL complete without error
- **AND** the resulting image SHALL have the application and its dependencies installed

#### Scenario: Container runs uvicorn on 0.0.0.0:8000
- **WHEN** the image is run with appropriate env vars (e.g. APP_ENV, DATABASE_URL, DEBUG)
- **THEN** the container SHALL start uvicorn serving the FastAPI app
- **AND** uvicorn SHALL bind to 0.0.0.0:8000 so the app is reachable from outside the container

#### Scenario: Container runs as non-root
- **WHEN** the container is running
- **THEN** the main process (uvicorn) SHALL run as a non-root user
- **AND** the image SHALL not require running as root to serve the application

#### Scenario: Configuration from environment
- **WHEN** the container is run
- **THEN** the application SHALL read APP_ENV, DATABASE_URL, and DEBUG from the container environment
- **AND** no default values in the image SHALL override explicitly set env vars at run time

### Requirement: Build context exclusions

The project SHALL provide a .dockerignore file so that unnecessary files are excluded from the Docker build context. This SHALL reduce build time and image size and avoid copying secrets or development-only files into the context.

#### Scenario: .dockerignore excludes common non-runtime paths
- **WHEN** the user runs `docker build`
- **THEN** the build context SHALL exclude at least: virtualenv directories (e.g. .venv), __pycache__, .git, .env (or similar env files that may contain secrets), and optionally openspec/changes, tests, or docs if they are not required to run the app
- **AND** the build context SHALL include the application code (e.g. app/), requirements.txt, and any files required at runtime (e.g. alembic if migrations are run from the same image)
