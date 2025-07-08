"""
Application configuration module.

Loads environment variables and nested settings using `pydantic-settings`.

Includes:
- BOT_TOKEN: Telegram bot token, loaded securely as a SecretStr
- database: nested configuration with SQLite async database URL

Configuration is loaded from a `.env` file, with nested fields separated using double underscores (`__`).
"""

import os
from pathlib import Path

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent


class Database(BaseModel):
    """
    Nested database configuration.
    """

    DB_URL: str = (
        f"sqlite+aiosqlite:///{os.path.abspath(BASE_DIR / 'database' / 'business_trips.db')}"
    )


class Settings(BaseSettings):
    """
    Main application settings loaded from environment variables.
    """

    BOT_TOKEN: SecretStr
    database: Database = Database()

    model_config = {"env_file": ".env", "env_nested_delimiter": "__"}


config = Settings()
