# FastAPI CRM - 12-factor, non-root, python:3.11-slim
FROM python:3.11-slim

WORKDIR /app

# Install pg_isready for entrypoint wait (then remove apt cache)
RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .
COPY docker/entrypoint.sh /app/docker/entrypoint.sh
COPY scripts ./scripts
RUN chmod +x /app/docker/entrypoint.sh

# Non-root user (UID 1000)
RUN adduser --disabled-password --gecos "" --uid 1000 appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Entrypoint: wait for DB, run migrations, then start uvicorn
ENTRYPOINT ["/app/docker/entrypoint.sh"]
