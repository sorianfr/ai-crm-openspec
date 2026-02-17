# Design: Docker image for FastAPI CRM

## Context

The app runs with uvicorn, reads APP_ENV/DATABASE_URL/DEBUG from env, and binds to 0.0.0.0. There is no Docker image today. We need a minimal Dockerfile and .dockerignore so the app can be built and run in containers without changing application code.

**Constraints:** python:3.11-slim; non-root user; 0.0.0.0:8000; 12-factor env only. No behavior changes.

## Goals / Non-Goals

**Goals:** Produce a working image from Dockerfile; exclude unneeded files via .dockerignore; run as non-root; use env vars for config.

**Non-Goals:** Multi-stage build (optional, can add later); docker-compose; production orchestration; CI/CD build pipeline.

## Decisions

### 1. Single-stage Dockerfile

**Decision:** Use a single-stage build: FROM python:3.11-slim, install deps, copy app, create non-root user, run uvicorn. No separate build stage unless needed for smaller image (slim is already small).

**Rationale:** Simplicity; requirements.txt has no build tools that need to be stripped. Can add multi-stage later if image size becomes an issue.

### 2. Non-root user

**Decision:** Create a user (e.g. `app` or `crm`) with a fixed UID in the image, own the app directory, and run uvicorn as that user. Do not run as root.

**Rationale:** Security best practice; matches proposal.

### 3. Working directory and copy

**Decision:** Set WORKDIR (e.g. /app). COPY requirements.txt first, run pip install, then COPY app and other needed paths (alembic, etc.). So layer caching works: deps change less often than code.

**Rationale:** Standard pattern; faster rebuilds when only code changes.

### 4. .dockerignore

**Decision:** Exclude .venv, __pycache__, .git, .env, *.pyc, openspec/changes (or whole openspec if not needed at runtime), .dockerignore, Dockerfile, README/docs/tests if not required to run the app. Include app/, alembic/, requirements.txt, and any file uvicorn or the app needs at runtime.

**Rationale:** Smaller context and image; no secrets in build; faster builds.

### 5. CMD/ENTRYPOINT

**Decision:** CMD runs uvicorn app.main:app --host 0.0.0.0 --port 8000. Port 8000 exposed via EXPOSE 8000. Env vars are provided at run time (docker run -e ... or compose).

**Rationale:** Matches 12-factor; no hardcoded config in image.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| SQLite in container loses data on restart | Document that production should set DATABASE_URL to a persistent volume or external DB. |
| Alembic in image | Include alembic so migrations can be run in the same image (e.g. as a separate run command); no requirement to run them in Dockerfile. |

## Migration Plan

Add Dockerfile and .dockerignore; document build/run in README. No rollout of app code. Users who already run without Docker are unaffected.

## Open Questions

None.
