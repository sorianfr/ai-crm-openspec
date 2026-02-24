# Docker compose dev/prod – verification

## Prerequisites

- Docker and Docker Compose installed
- For prod: copy `.env.prod.example` to `.env.prod` and set `JWT_SECRET`, `SESSION_SECRET`, and `DATABASE_URL` (real values)

## Dev

1. **Start stack**

   ```bash
   docker compose -f docker-compose.dev.yml up --build
   ```

2. **Checks**

   - App starts without manually running `alembic upgrade head` (migrations run in entrypoint).
   - Open http://localhost:8000/health → expect 200 and healthy response.
   - Open http://localhost:8000/login → log in (e.g. dev seed user if present); session should persist (cookie).

3. **Stop**

   ```bash
   docker compose -f docker-compose.dev.yml down
   ```

## Prod

1. **Prepare env**

   ```bash
   cp .env.prod.example .env.prod
   # Edit .env.prod: set JWT_SECRET, SESSION_SECRET, DATABASE_URL (and POSTGRES_PASSWORD in compose if needed)
   ```

2. **Start stack**

   ```bash
   docker compose -f docker-compose.prod.yml up -d --build
   ```

3. **Checks**

   - App starts and runs migrations automatically (check logs for `alembic upgrade head`).
   - `JWT_SECRET` and `SESSION_SECRET` must be set or app fails fast.
   - Postgres port 5432 is not published to the host (no `5432:5432` in prod compose).
   - http://localhost:8000/health returns 200.

4. **Stop**

   ```bash
   docker compose -f docker-compose.prod.yml down
   ```
