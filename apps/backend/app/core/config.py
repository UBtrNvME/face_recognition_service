# app/core/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "FastAPI Monorepo Backend"
    environment: str = "development"

    database_url: str
    
    # JWT Settings
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
