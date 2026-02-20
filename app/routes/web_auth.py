"""Web login/logout routes (cookie session). JWT /auth/login unchanged for API."""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.csrf import ensure_csrf_token, rotate_csrf_token, validate_csrf_or_403
from app.core.password import verify_password
from app.core.templates import templates
from app.db.session import get_db
from app.models import User

router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    """Render login form."""
    csrf_token = ensure_csrf_token(request)
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "csrf_token": csrf_token, "error": None},
    )


@router.post("/login")
def login_post(
    request: Request,
    db: Session = Depends(get_db),
    email: str = Form(""),
    password: str = Form(""),
    csrf_token: str | None = Form(None),
):
    """Validate credentials; on success set session, rotate CSRF, redirect to /."""
    token = csrf_token or request.headers.get("X-CSRF-Token")
    validate_csrf_or_403(request, token)

    user = (
        db.execute(select(User).where(User.email == email.strip())).scalars().first()
    )
    if user is None or not verify_password(password, user.password_hash):
        csrf_token_val = ensure_csrf_token(request)
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "csrf_token": csrf_token_val,
                "error": "Invalid email or password",
            },
            status_code=200,
        )
    request.session["user_id"] = user.id
    rotate_csrf_token(request)
    return RedirectResponse(url="/", status_code=303)


@router.post("/logout")
def logout(request: Request) -> RedirectResponse:
    """Clear session and redirect to /login."""
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)
