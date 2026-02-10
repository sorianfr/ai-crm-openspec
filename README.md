# Python CRM – Bootstrap

Technical foundation for a Python web application: FastAPI, SQLite, SQLAlchemy, Alembic, Jinja2, and HTMX.

## Setup

1. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Copy environment example and adjust if needed:

   ```bash
   cp .env.example .env
   ```

3. (Optional) Run database migrations:

   ```bash
   alembic upgrade head
   ```

4. Run the application:

   ```bash
   uvicorn app.main:app --reload
   ```

5. Open in browser:

   - Homepage: http://localhost:8000/
   - Health: http://localhost:8000/health
   - API docs: http://localhost:8000/docs

## Project structure

- `app/main.py` – FastAPI application entry point
- `app/core/config.py` – Configuration
- `app/db/` – Database session and base
- `app/routes/` – Health and home routes
- `app/templates/` – Jinja2 templates (HTMX via CDN in base)
- `app/static/` – Static assets
