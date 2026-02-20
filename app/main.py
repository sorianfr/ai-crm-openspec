"""FastAPI application entry point."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import APP_ENV, SESSION_MAX_AGE, SESSION_SECRET
from app.core.web_auth import RedirectToLoginException
from app.core.csrf_middleware import CSRFTokenMiddleware
from app.routes import auth, companies, contacts, health, home, users, web_auth

app = FastAPI(
    title="Python CRM",
    description="Technical foundation: FastAPI, SQLite, Jinja2, HTMX",
    version="0.1.0",
)

# Order: add CSRF first, then Session - so Session runs first (outermost), then CSRF has session
app.add_middleware(CSRFTokenMiddleware)
app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET,
    max_age=SESSION_MAX_AGE,
    same_site="lax",
    https_only=(APP_ENV == "production"),
)

# Static files: app/static/
static_dir = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Routes
app.include_router(health.router, tags=["health"])
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(web_auth.router, tags=["web-auth"])
app.include_router(home.router, tags=["home"])
app.include_router(contacts.router, tags=["contacts"])
app.include_router(companies.router, tags=["companies"])


@app.exception_handler(RedirectToLoginException)
async def redirect_to_login_handler(request, exc):
    return RedirectResponse(url="/login", status_code=303)


@app.on_event("startup")
async def startup() -> None:
    """Application startup: optional dev seed when APP_ENV=development."""
    from app.core.seed import seed_dev_admin_if_needed_sync
    seed_dev_admin_if_needed_sync()


@app.on_event("shutdown")
async def shutdown() -> None:
    """Application shutdown (optional future use)."""
    pass
