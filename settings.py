import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, BaseModel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Database(BaseModel):
    DB_URL: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=os.path.join(BASE_DIR, ".env"),
        env_file_encoding="utf-8",
        env_nested_delimiter="__",  # This enables nested loading
    )

    BOT_TOKEN: SecretStr
    database: Database


config = Settings()
