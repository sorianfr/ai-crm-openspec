# Python CRM -- Bootstrap

Technical foundation for a Python CRM application built with:

-   FastAPI
-   PostgreSQL (production) / SQLite (development)
-   SQLAlchemy
-   Alembic
-   Jinja2
-   HTMX
-   Tailwind (via CDN)

The application follows **12-factor principles**:

-   Configuration via environment variables
-   Production-safe defaults
-   Container-friendly server binding (`0.0.0.0`)

------------------------------------------------------------------------

## Environment Variables

The application reads configuration from environment variables.

  --------------------------------------------------------------------------
  Variable                   Description                     Default (dev only)
  -------------------------  ------------------------------  ------------------
  `APP_ENV`                  development, staging, production  development
  `DATABASE_URL`             SQLAlchemy connection string    SQLite (dev only)
  `JWT_SECRET`               Secret for JWT signing (auth)   (none; set in prod)
  `JWT_EXPIRATION_MINUTES`   Access token lifetime (minutes) 60
  `DEBUG`                    Enable debug mode               false
  --------------------------------------------------------------------------

------------------------------------------------------------------------

### Production Rule

When:

APP_ENV=production

`DATABASE_URL` **must be explicitly set**.

The application will **fail fast on startup** if `DATABASE_URL` is
missing.

Example PostgreSQL URL:

postgresql+psycopg://user:pass@host:5432/dbname

------------------------------------------------------------------------

## Local Development Setup

### 1️⃣ Create virtual environment and install dependencies

python -m venv .venv source .venv/bin/activate \# Windows:
.venv`\Scripts`{=tex}`\activate`{=tex} pip install -r requirements.txt

### 2️⃣ Copy environment example

cp .env.example .env

Adjust variables inside `.env` if needed.

### 3️⃣ Run database migrations

alembic upgrade head

### 4️⃣ Run the application

uvicorn app.main:app --host 0.0.0.0 --port 8000

### 5️⃣ Open in browser

-   Homepage: http://localhost:8000/
-   Health: http://localhost:8000/health
-   API docs: http://localhost:8000/docs

------------------------------------------------------------------------

## Project Structure

app/ main.py → FastAPI entrypoint core/config.py → Environment-based
configuration (12-factor) db/ → Database session & base models/ →
SQLAlchemy models routes/ → Application routes templates/ → Jinja2
templates (HTMX + Tailwind CDN) static/ → Static assets

alembic/ → Database migrations requirements.txt → Python dependencies

------------------------------------------------------------------------

## Deployment Notes

-   SQLite is used automatically in development if `DATABASE_URL` is not
    set.
-   PostgreSQL is recommended for production.
-   The app binds to `0.0.0.0` so it works inside Docker and Kubernetes.
-   Alembic should be run during deployment before serving traffic.
-   In production, ensure `APP_ENV=production` and `DATABASE_URL` is
    properly configured.
-   To verify PostgreSQL connectivity, run the app or `alembic upgrade head`
    with `DATABASE_URL=postgresql+psycopg://...` when a Postgres instance is
    available.
