from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # class Config:
    #     env_file = ".env"
    #     env_file_encoding = "utf-8"
    #     env_prefix = "app_"
    #     case_sensitive = False

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="app_"
    )

    database_url: str | None = None


settings = Settings()
print(settings.model_dump())
