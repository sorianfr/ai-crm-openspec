"""FastAPI application entry point."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import health, home, contacts

app = FastAPI(
    title="Python CRM",
    description="Technical foundation: FastAPI, SQLite, Jinja2, HTMX",
    version="0.1.0",
)

# Static files: app/static/
static_dir = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Routes
app.include_router(health.router, tags=["health"])
app.include_router(home.router, tags=["home"])
app.include_router(contacts.router, tags=["contacts"])


@app.on_event("startup")
async def startup() -> None:
    """Application startup (optional future use)."""
    pass


@app.on_event("shutdown")
async def shutdown() -> None:
    """Application shutdown (optional future use)."""
    pass
