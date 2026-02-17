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

# Project root (for resolving paths relative to project)
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent
