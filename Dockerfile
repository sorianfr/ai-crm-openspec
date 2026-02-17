# FastAPI CRM - 12-factor, non-root, python:3.11-slim
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .

# Non-root user (UID 1000)
RUN adduser --disabled-password --gecos "" --uid 1000 appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# 12-factor: APP_ENV, DATABASE_URL, DEBUG from environment
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
