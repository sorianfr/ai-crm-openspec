# Design: Docker Compose dev/prod

## Context

The app has a single `docker-compose.yml` with inline env and no entrypoint. Startups can fail due to: migrations not run before the app; missing or inconsistent secrets (JWT_SECRET, SESSION_SECRET); and cookie/security settings (Secure flag) that don’t match dev (HTTP localhost) vs prod (HTTPS behind a proxy). The Dockerfile runs Uvicorn directly with no DB wait or migration step. We need a reproducible dev and prod Docker setup with clear env separation and automated migrations on start.

## Goals / Non-Goals

**Goals:**

- Two Compose configs (dev and prod) with appropriate env and port exposure.
- Single app entrypoint: wait for Postgres → run migrations → start Uvicorn.
- Env via `.env.dev` / `.env.prod` (prod template committed as `.env.prod.example`).
- Reliable container runs: bcrypt/passlib compatibility and consistent `DATABASE_URL` (e.g. `postgresql+psycopg://...`) for app and Alembic.
- README run commands for both environments.

**Non-Goals:**

- Adding a reverse proxy in this change (optional later).
- Committing real secrets in `.env.dev` or `.env.prod` (safe defaults in `.env.dev` are acceptable).

## Decisions

### File layout

- **`docker-compose.dev.yml`** – development Compose (ports exposed, dev env).
- **`docker-compose.prod.yml`** – production Compose (no Postgres port, prod env).
- **`.env.dev`** – dev env vars; safe defaults OK; not committed if it ever holds secrets (or gitignored).
- **`.env.prod.example`** – committed template for prod; real `.env.prod` not committed.
- **`docker/entrypoint.sh`** – app container entrypoint: wait for DB → `alembic upgrade head` → Uvicorn.

*Rationale:* Separating dev/prod files avoids mixing env and port exposure; entrypoint centralizes startup order so migrations always run before the app.

### Development Compose (`docker-compose.dev.yml`)

- `APP_ENV=development`, `DEBUG=true`.
- Cookie `Secure=false` (works over `http://localhost`).
- Expose ports **8000** (app) and **5432** (Postgres) for local tools (e.g. DB clients).
- Named volume for Postgres data.
- `env_file: .env.dev`.

*Rationale:* Dev needs direct DB access and non-Secure cookies; env_file keeps vars out of the compose file and allows local overrides.

### Production Compose (`docker-compose.prod.yml`)

- `APP_ENV=production`, `DEBUG=false`.
- Cookie `Secure=true` (assumes HTTPS at reverse proxy).
- Do **not** expose Postgres port (no `5432` host mapping).
- `env_file: .env.prod` (not committed); provide `.env.prod.example` with required keys and placeholders.
- Reverse proxy is out of scope; can be added later.

*Rationale:* Prod must not expose the DB; Secure cookies and no DEBUG reduce risk; example file documents required vars without committing secrets.

### Entrypoint (`docker/entrypoint.sh`)

1. Wait for DB: loop using `pg_isready` (or equivalent) until Postgres is accepting connections.
2. Run: `alembic upgrade head`.
3. Start: `uvicorn app.main:app --host 0.0.0.0 --port 8000`.

*Rationale:* Ensures DB is up and schema is migrated before the app starts; single script keeps behavior consistent across dev and prod. Alternative of running migrations in a one-off container is possible but adds orchestration; entrypoint is simpler for single-app compose.

### Dependencies and DATABASE_URL

- Pin **`bcrypt<4`** in `requirements.txt` to avoid passlib/bcrypt runtime issues in the container.
- Use one driver format for `DATABASE_URL` everywhere (e.g. **`postgresql+psycopg://...`** for psycopg v3); same value in compose env, app config, and Alembic.

*Rationale:* bcrypt 4.x can break passlib; pinning avoids image-specific failures. Single `DATABASE_URL` format prevents “works locally, fails in Docker” due to driver mismatch.

## Verification

- **Dev:** `docker compose -f docker-compose.dev.yml up --build`
  - App starts without manually running Alembic.
  - `/health` returns OK.
  - `/login` works and session persists (cookie).
- **Prod:** `docker compose -f docker-compose.prod.yml up --build`
  - App starts and runs migrations automatically.
  - Requires `JWT_SECRET` and `SESSION_SECRET` set (e.g. via `.env.prod` or env).

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Entrypoint runs as non-root; `pg_isready`/alembic must be on PATH | Use image that includes Postgres client or install minimal client in Dockerfile; keep entrypoint simple. |
| Migrations fail → container exits | Entrypoint exits on failure; orchestration restarts or alerts; ensure migration errors are visible in logs. |
| `.env.prod` forgotten or wrong | Document in README and `.env.prod.example`; consider startup check that fails fast if required vars missing. |
| bcrypt pin may lag security updates | Pin only as needed (e.g. `bcrypt<4`); track passlib/bcrypt compatibility for future unpin. |

## Migration Plan

- Add new files (compose, env examples, entrypoint); no change to existing app code paths beyond env usage.
- Update Dockerfile: install entrypoint deps if needed, set `ENTRYPOINT`/`CMD` to use `docker/entrypoint.sh`.
- Add `bcrypt<4` to `requirements.txt`.
- README: add “Run dev” and “Run prod” sections with the two `docker compose -f ...` commands and note required prod env vars.
- Existing `docker-compose.yml` can remain for backward compatibility or be deprecated in README in favor of dev/prod files.

## Open Questions

- Whether to keep the current `docker-compose.yml` as an alias for dev (e.g. default `docker compose up`) or remove it once dev/prod are stable.
- Whether to add a healthcheck for the app service in compose (e.g. GET `/health`) for `depends_on` and restarts.
