"""Application configuration loaded from environment variables."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Database: SQLite file created on first connection or when migrations run
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Debug mode
DEBUG: bool = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")

# Project root (for resolving paths relative to project)
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent
