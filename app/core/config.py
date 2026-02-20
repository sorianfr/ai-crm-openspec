"""Application configuration loaded from environment variables (12-factor)."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(".env.local")

# Environment: development, staging, production
APP_ENV: str = os.getenv("APP_ENV", "development")

# Database: SQLite default for non-production; production must set DATABASE_URL
def _get_database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if APP_ENV == "production":
        if not url or not url.strip():
            raise RuntimeError(
                "DATABASE_URL must be set when APP_ENV=production. "
                "Set the environment variable before starting the application."
            )
        return url.strip()
    return url.strip() if url and url.strip() else "sqlite:///./app.db"


DATABASE_URL: str = _get_database_url()

# Debug mode (default false for production safety)
DEBUG: bool = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")

# JWT: secret and expiration (required for auth; use strong secret in production)
JWT_SECRET: str = os.getenv("JWT_SECRET", "")
JWT_EXPIRATION_MINUTES: int = int(os.getenv("JWT_EXPIRATION_MINUTES", "60"))
JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")

# Session (web UI cookie auth; required in production)
def _get_session_secret() -> str:
    secret = os.getenv("SESSION_SECRET", "").strip()
    if APP_ENV == "production":
        if not secret:
            raise RuntimeError(
                "SESSION_SECRET must be set when APP_ENV=production. "
                "Set the environment variable before starting the application."
            )
        return secret
    return secret or "dev-session-secret-change-in-production"


SESSION_SECRET: str = _get_session_secret()
SESSION_MAX_AGE: int = int(os.getenv("SESSION_MAX_AGE", "28800"))  # 8 hours default

# Project root (for resolving paths relative to project)
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent
