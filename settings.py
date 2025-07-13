from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings


class Database(BaseModel):
    DB_URL: str


class Settings(BaseSettings):
    ENV: str
    BOT_TOKEN: SecretStr
    database: Database

    model_config = {"env_file": ".env", "env_nested_delimiter": "__"}  # if __ in .env, [0] is object, [1] is field


config = Settings()
