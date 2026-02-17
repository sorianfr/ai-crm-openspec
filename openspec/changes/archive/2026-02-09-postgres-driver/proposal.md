# Add PostgreSQL driver support

## Why

The app is 12-factor and supports DATABASE_URL; production is expected to use PostgreSQL. Today only SQLite is wired (no PostgreSQL driver). Adding the PostgreSQL driver lets production set DATABASE_URL to a postgres URL and run the same codebase against PostgreSQL. No change to SQLite behavior; this is additive.

## What Changes

- **Driver dependency:** Add the PostgreSQL adapter for SQLAlchemy (psycopg v3: `psycopg[binary]>=3.1`) to requirements.txt so that `postgresql+psycopg://` URLs work.
- **Session/engine:** Ensure the database session and engine work with PostgreSQL when DATABASE_URL is a postgres URL (no SQLite-specific assumptions that break postgres). SQLite-specific logic (e.g. connect_args, foreign_keys) SHALL remain conditional on SQLite.
- **Documentation:** Document that production can set DATABASE_URL to a PostgreSQL URL (e.g. `postgresql+psycopg://user:pass@host:5432/dbname`).
- **No behavior changes:** Existing SQLite usage and behavior unchanged. No schema or API changes.

## Capabilities

### New Capabilities

- None

### Modified Capabilities

- **database-setup:** The system SHALL support both SQLite and PostgreSQL as backends. When DATABASE_URL is a PostgreSQL URL, the application SHALL connect using the installed PostgreSQL driver. SQLite SHALL remain supported when DATABASE_URL is a SQLite URL.

## Impact

- **requirements.txt:** Add psycopg[binary]>=3.1 (psycopg v3).
- **app/db/session.py:** Keep SQLite-only connect_args and events conditional; no postgres-specific code required if driver handles it, or add any minimal engine options for postgres if needed.
- **README/docs:** Mention PostgreSQL and example DATABASE_URL.
- **Dockerfile:** No change (already uses requirements.txt; driver will be installed).
