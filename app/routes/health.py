"""Health check endpoint."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    """Return service status for monitoring and readiness checks."""
    return {"status": "ok"}
