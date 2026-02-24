#!/usr/bin/env bash
set -e

# Wait for Postgres (host=db, user/db from env or default crm)
DB_HOST="${DB_HOST:-db}"
DB_USER="${DB_USER:-crm}"
DB_NAME="${DB_NAME:-crm}"
until pg_isready -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME"; do
  echo "Waiting for Postgres at $DB_HOST..."
  sleep 1
done

echo "Running migrations..."
alembic upgrade head

echo "Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
