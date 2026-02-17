# Make app 12-factor: config from env, production defaults, container-friendly bind

## Why

The app should follow 12-factor configuration and be deployable in containers without code or default changes. Configuration from environment variables (DATABASE_URL, DEBUG, APP_ENV), production-ready defaults, and uvicorn binding to 0.0.0.0 make the app suitable for production and containerized environments. No change to application behavior—only where config comes from and how the server is bound.

## What Changes

- **Config from environment:** Application configuration SHALL be read from environment variables: `DATABASE_URL` (database connection string), `DEBUG` (boolean), `APP_ENV` (e.g. development, staging, production). Existing use of `DATABASE_URL` and `DEBUG` remains; `APP_ENV` is added.
- **Production-ready defaults:** Defaults when env vars are unset SHALL be safe for production (e.g. DEBUG default false, DATABASE_URL default remains or is explicitly documented as dev-only where appropriate). When APP_ENV=production, DATABASE_URL MUST be explicitly set. The application SHALL fail fast on startup if DATABASE_URL is missing. When APP_ENV is not production, the application MAY default to a development SQLite database.
- **Uvicorn bind for containers:** When the app is run via uvicorn (e.g. `uvicorn app.main:app`), it SHALL bind to `0.0.0.0` so it is reachable from outside the container/host. This MAY be done via a default in a run script, `pyproject.toml` script, or documentation so that `uvicorn ... --host 0.0.0.0` is the standard way to run the app.
- **No behavior changes:** No change to routes, templates, or business logic; only configuration source and server bind address.

## Capabilities

### New Capabilities

- None

### Modified Capabilities

- **fastapi-project-structure:** Config module SHALL load DATABASE_URL, DEBUG, and APP_ENV from environment with production-safe defaults; run contract (uvicorn) SHALL support binding to 0.0.0.0 for container deployment.

## Impact

- **app/core/config.py:** Add APP_ENV; ensure DEBUG and DATABASE_URL defaults are production-safe (or document dev-only defaults).
- **Run / entrypoint:** Ensure uvicorn is invoked with `--host 0.0.0.0` (e.g. in `pyproject.toml` scripts, Makefile, or README/docker instructions). No change to app/main.py behavior unless needed to read config for host/port.
- **Dependencies:** No new dependencies.
- **Documentation:** Optional: document env vars and 0.0.0.0 for containers.
