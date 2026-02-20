"""CSRF protection for cookie-authenticated web routes."""

import secrets

from fastapi import HTTPException, Request


def generate_csrf_token() -> str:
    """Generate a random CSRF token."""
    return secrets.token_urlsafe(32)


def ensure_csrf_token(request: Request) -> str:
    """Ensure session has csrf_token; generate and store if missing. Return token."""
    token = request.session.get("csrf_token")
    if not token:
        token = generate_csrf_token()
        request.session["csrf_token"] = token
    return token


def rotate_csrf_token(request: Request) -> str:
    """Generate new CSRF token, store in session, return it."""
    token = generate_csrf_token()
    request.session["csrf_token"] = token
    return token


def validate_csrf(request: Request, token: str | None) -> bool:
    """Validate token against session. Return True if valid, False otherwise."""
    if not token:
        return False
    return secrets.compare_digest(token, request.session.get("csrf_token", ""))


def validate_csrf_or_403(request: Request, token: str | None) -> None:
    """Raise 403 if token invalid. Call from mutation routes with csrf_token from Form."""
    if not validate_csrf(request, token):
        raise HTTPException(status_code=403, detail="Invalid or missing CSRF token")
