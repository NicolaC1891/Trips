from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings


class DatabaseConfig(BaseModel):
    DB_URL: str


class TelegramConfig(BaseModel):
    BOT_TOKEN: SecretStr


class BotConfig(BaseSettings):
    ENV: str
    TELEGRAM: TelegramConfig
    DATABASE: DatabaseConfig

    model_config = {
        "env_file": ".env",
        "env_nested_delimiter": "__",
    }


config = BotConfig()

print(config)
