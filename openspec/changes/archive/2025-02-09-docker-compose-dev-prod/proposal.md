## Why

We need a reliable, reproducible Docker setup that works locally (dev) and in production (prod) without manual steps. Today the app can fail on startup due to missing migrations, missing secrets, and different cookie/security expectations (SESSION/JWT secrets, Secure cookies).

## What Changes

- Introduce two Docker Compose configs:
  - Development: `docker-compose.dev.yml`
  - Production: `docker-compose.prod.yml`
- Standardize environment variables using `.env.dev` and `.env.prod` (or env_file blocks)
- Add an app entrypoint that:
  1) waits for Postgres
  2) runs `alembic upgrade head`
  3) starts Uvicorn
- Fix bcrypt/passlib compatibility in Docker by pinning `bcrypt<4`
- Ensure both Alembic and app use the same `DATABASE_URL` from environment
- Add clear run commands in README

## Capabilities

### New Capabilities

- `docker-runtime-config`: reproducible dev/prod docker-compose configuration and env management

### Modified Capabilities

- `database-setup`: docker + postgres runtime expectations (migrations on start)
- `fastapi-project-structure`: container startup flow (entrypoint)

## Impact

- New compose files + env files
- Updated Dockerfile/entrypoint (startup behavior)
- requirements.txt pin for bcrypt
- README updates
