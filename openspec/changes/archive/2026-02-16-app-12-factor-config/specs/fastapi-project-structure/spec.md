## ADDED Requirements

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
