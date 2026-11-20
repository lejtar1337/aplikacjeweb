from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TASKBOARD_", env_file=".env")

    app_title: str = "TaskBoard"
    cors_origins: list[str] = ["http://127.0.0.1:5500"]


settings = Settings()
