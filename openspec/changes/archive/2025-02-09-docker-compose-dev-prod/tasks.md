## 1. Dependencies and entrypoint

- [x] 1.1 Add bcrypt<4 to requirements.txt
- [x] 1.2 Add docker/entrypoint.sh (wait-for-db + alembic upgrade head + uvicorn)
- [x] 1.3 Update Dockerfile to copy entrypoint.sh and set ENTRYPOINT/CMD properly

## 2. Compose and environment files

- [x] 2.1 Create docker-compose.dev.yml (db + app, ports exposed, env_file .env.dev)
- [x] 2.2 Create docker-compose.prod.yml (db + app, no postgres port published, env_file .env.prod)
- [x] 2.3 Add .env.dev (safe defaults for local) and .env.prod.example (template)

## 3. Documentation and verification

- [x] 3.1 Update README with run commands: Dev: `docker compose -f docker-compose.dev.yml up --build`; Prod: `docker compose -f docker-compose.prod.yml up -d --build`
- [x] 3.2 Add VERIFICATION.md for this change with verification steps
