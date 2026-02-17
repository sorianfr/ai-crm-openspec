# Dockerize the FastAPI CRM

## Why

The app is 12-factor ready (config from env, uvicorn on 0.0.0.0) but has no container image. Adding a Dockerfile lets teams run the CRM in Docker, Kubernetes, or any container platform with a single, repeatable image. Using python:3.11-slim keeps the image small; a non-root user and env-based config keep the container secure and portable. No change to application behavior—only packaging and run environment.

## What Changes

- **Dockerfile:** Add a Dockerfile based on `python:3.11-slim`. Install dependencies from requirements.txt, copy application code, and run uvicorn bound to `0.0.0.0:8000`. Use a non-root user inside the container.
- **.dockerignore:** Add .dockerignore to exclude unnecessary files from the build context (e.g. .venv, __pycache__, .git, .env, openspec/changes, tests, docs).
- **12-factor in container:** The container SHALL expect env vars `APP_ENV`, `DATABASE_URL`, and `DEBUG` (same as current app config). No hardcoded defaults that override env; document or example only.
- **No behavior changes:** No change to routes, config module, or business logic; only container image and run instructions.

## Capabilities

### New Capabilities

- **docker-packaging:** The project SHALL provide a Docker image build (Dockerfile and .dockerignore). The image SHALL be based on python:3.11-slim, run the FastAPI app via uvicorn on 0.0.0.0:8000, use a non-root user, and rely on 12-factor env vars (APP_ENV, DATABASE_URL, DEBUG) for configuration.

### Modified Capabilities

- None

## Impact

- **New files:** `Dockerfile`, `.dockerignore`
- **Dependencies:** None (existing requirements.txt used in image)
- **Documentation:** Optional: add "Run with Docker" to README (e.g. build, run with env vars, port 8000)
- **CI/CD:** Can add build/push in a later change; out of scope here.
