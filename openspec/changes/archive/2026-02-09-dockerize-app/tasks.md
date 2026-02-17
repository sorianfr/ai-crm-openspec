## 1. Dockerfile

- [x] 1.1 Add Dockerfile based on python:3.11-slim; install dependencies from requirements.txt, copy app and required paths (app/, alembic/, etc.), set WORKDIR
- [x] 1.2 Create non-root user in the image and run uvicorn as that user; CMD uvicorn app.main:app --host 0.0.0.0 --port 8000; EXPOSE 8000

## 2. .dockerignore

- [x] 2.1 Add .dockerignore excluding .venv, __pycache__, .git, .env, *.pyc, and other non-runtime paths; ensure app/, requirements.txt, and runtime-needed files are not excluded

## 3. Verification

- [x] 3.1 Verify docker build succeeds and container runs (e.g. docker run with APP_ENV=development DATABASE_URL=sqlite:///./app.db); app responds on port 8000
- [x] 3.2 Verify process in container runs as non-root (e.g. whoami or id in running container)
