"""Session-based auth for web UI. JWT auth (app.core.auth) unchanged for API."""

from fastapi import Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette import status

from app.db.session import get_db
from app.models import User


class RedirectToLoginException(Exception):
    """Raised when web user must be redirected to /login."""

    def __init__(self) -> None:
        super().__init__("Redirect to login")


def get_current_web_user(
    request: Request,
    db: Session = Depends(get_db),
) -> User:
    """Resolve user from session user_id; raise RedirectToLoginException if missing or invalid."""
    user_id = request.session.get("user_id")
    if not user_id:
        raise RedirectToLoginException()
    try:
        uid = int(user_id)
    except (TypeError, ValueError):
        request.session.clear()
        raise RedirectToLoginException()
    user = db.get(User, uid)
    if user is None:
        request.session.clear()
        raise RedirectToLoginException()
    return user


def require_web_roles(allowed_roles: list[str]):
    """Dependency: require current web user role; 403 if not allowed (no redirect for HTMX)."""

    def _check(
        current_user: User = Depends(get_current_web_user),
    ) -> User:
        if current_user.role in allowed_roles:
            return current_user
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")

    return _check
