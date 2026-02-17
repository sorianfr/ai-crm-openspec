# Design: PostgreSQL driver support

## Context

The app uses SQLAlchemy with a single DATABASE_URL. Session and engine are in app/db/session.py; SQLite uses connect_args (check_same_thread) and a connect event for foreign_keys. There is no PostgreSQL driver in requirements.txt today.

**Constraints:** No breaking change to SQLite. Add driver so postgres URLs work.

## Goals / Non-Goals

**Goals:** Add PostgreSQL driver dependency; ensure create_engine(DATABASE_URL) works for postgres URLs; keep SQLite behavior as-is.

**Non-Goals:** Async driver (asyncpg); connection pooling tuning; multi-database switching at runtime.

## Decisions

### 1. Which driver

**Decision:** Add `psycopg[binary]>=3.1` (psycopg v3) to requirements.txt. Use `postgresql+psycopg://` in DATABASE_URL. Psycopg v3 is the current recommended driver for SQLAlchemy + PostgreSQL.

**Rationale:** Psycopg 3 is the modern driver; binary extra avoids system libpq build. Same SQLAlchemy create_engine usage.

### 2. Session/engine code

**Decision:** No change to session.py required for basic postgres support. create_engine(DATABASE_URL) works with postgres when the driver is installed. Keep existing SQLite-only branches (connect_args, PRAGMA foreign_keys) strictly conditional on DATABASE_URL.startswith("sqlite"). Do not add postgres-specific connect_args unless needed (e.g. for SSL or timeouts later).

**Rationale:** SQLAlchemy + psycopg v3 works out of the box. Minimal change.

### 3. Alembic

**Decision:** Alembic already uses the same DATABASE_URL (from config). Once the driver is installed, `alembic upgrade head` with a postgres DATABASE_URL will work. No Alembic code change.

**Rationale:** env.py uses config; migrations are backend-agnostic for this app.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| psycopg binary extra not ideal for some production deployments | Document that production may use psycopg without [binary] if policy requires; same API. |

## Migration Plan

Add dependency; optionally document postgres URL. No data migration. Deploy with new requirements; set DATABASE_URL to postgres in production when ready.

## Open Questions

None.
