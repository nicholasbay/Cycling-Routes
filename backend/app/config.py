from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_TITLE: str = "PitStop API"
    APP_DESCRIPTION: str = "API for planning cycling routes that stay within bike-sharing time limits."
    APP_VERSION: str = "1.0.0"

    DATAMALL_ACCOUNT_KEY: str
    ONEMAP_BASE_URL: str
    ONEMAP_EMAIL: str
    ONEMAP_PASSWORD: str

    POSTGRES_HOST: str
    POSTGRES_PORT: str = '5432'
    POSTGRES_DATABASE: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings():
    return Settings()
