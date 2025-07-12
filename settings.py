from pathlib import Path
import os
from dotenv import load_dotenv

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / ".env")


class Database(BaseModel):
    DB_URL: str = (
        f"sqlite+aiosqlite:///{os.path.abspath(BASE_DIR / 'database' / 'business_trips.db')}"
    )

class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    database: Database = Database()

    model_config = {"env_file": ".env", "env_nested_delimiter": "__"}

config = Settings()