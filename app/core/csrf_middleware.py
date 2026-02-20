"""Middleware to inject csrf_token into request.state. Must run after SessionMiddleware."""

from starlette.middleware.base import BaseHTTPMiddleware

from app.core.csrf import ensure_csrf_token


class CSRFTokenMiddleware(BaseHTTPMiddleware):
    """Add request.state.csrf_token for templates. Requires SessionMiddleware to run first."""

    async def dispatch(self, request, call_next):
        request.state.csrf_token = ensure_csrf_token(request)
        return await call_next(request)
