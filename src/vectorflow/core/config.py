from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    PROJECT_NAME: str = "VectorFlow"
    ENVIRONMENT: Literal["development", "testing", "production"] = "development"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = 'dev_secret_key_change_in_production_min_32_chars'

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "vectorflow"

    REDIS_PORT: int = 6379
    REDIS_HOST: str = "localhost"

    @computed_field
    @property
    def REDIS_URL(self) -> str:
        """Redis Connection String"""
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"
       
    @computed_field
    @property
    def ASYNC_DATABASE_URI(self) -> str:
        return (
                f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

@lru_cache
def get_settings() -> "Settings":
    """Returns cached instance of the settings singleton"""
    return Settings()