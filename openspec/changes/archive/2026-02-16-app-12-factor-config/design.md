# Design: 12-factor config and container bind

## Context

The app already reads DATABASE_URL and DEBUG from environment (app/core/config.py) with defaults. It uses python-dotenv for local .env. There is no APP_ENV; uvicorn is typically run ad hoc (e.g. `uvicorn app.main:app`) and may bind to 127.0.0.1 by default, which is not suitable for containers.

**Constraints:** No behavior change to routes or business logic. Config and run contract only.

## Goals / Non-Goals

**Goals:** Add APP_ENV; keep production-safe defaults (DEBUG=false, optional fail-fast for DATABASE_URL when APP_ENV=production per proposal); make the standard run use uvicorn with --host 0.0.0.0 for containers.

**Non-Goals:** Changing how the app uses DEBUG or DATABASE_URL in code; adding new runtime behavior beyond config and bind.

## Decisions

### 1. APP_ENV and defaults

**Decision:** Add APP_ENV = os.getenv("APP_ENV", "development"). Treat "production" as production; anything else (development, staging, test) keeps current relaxed defaults. When APP_ENV is "production", require DATABASE_URL to be set (no default or fail at startup). When not production, keep default DATABASE_URL (e.g. sqlite:///./app.db) so local dev works without env.

**Rationale:** Matches proposal: production-safe, fail-fast in production if DATABASE_URL missing; dev-friendly otherwise.

### 2. Uvicorn bind 0.0.0.0

**Decision:** Provide a standard run path that uses --host 0.0.0.0 (e.g. script in pyproject.toml, Makefile target, or documented command). Do not hardcode host inside app/main.py unless the app reads config and passes it to uvicorn programmatically; prefer external run contract (script or docs) so `uvicorn app.main:app --host 0.0.0.0` is the default way to run.

**Rationale:** 12-factor: config in env; process binding is part of the run contract. Keeping it in the run script/docs avoids coupling the FastAPI app to a specific host.

### 3. load_dotenv()

**Decision:** Keep load_dotenv() in config so local development can use .env. In production, env vars are set by the platform; load_dotenv() is a no-op when .env is absent. No change.

**Rationale:** No behavior change; dev experience preserved.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Production deploy forgets DATABASE_URL | When APP_ENV=production, fail fast if DATABASE_URL is missing (per proposal). |
| Port not configurable | Out of scope; 0.0.0.0 only. Port can be added later via PORT env if needed. |

## Migration Plan

Deploy config and run changes; set APP_ENV and DATABASE_URL in production. No data migration. Rollback: revert code and run with previous command.

## Open Questions

None.
