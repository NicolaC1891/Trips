from pydantic_settings import BaseSettings
from pydantic import BaseModel, SecretStr
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

class Database(BaseModel):
    # Значение по умолчанию: для локальной машины
    DB_URL: str = f"sqlite+aiosqlite:///{os.path.abspath(BASE_DIR / 'database' / 'business_trips.db')}"

class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    database: Database = Database()

    model_config = {
        "env_file": ".env",
        "env_nested_delimiter": "__"
    }

config = Settings()