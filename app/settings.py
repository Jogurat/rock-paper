from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int = 5432
    postgres_db: str

    redis_url: str
    redis_port: int = 6379

    random_number_url: str = "https://codechallenge.boohma.com/random"

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def settings():
    return Settings()
