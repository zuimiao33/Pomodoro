from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    app_name: str = "todo-pomodoro-api"
    app_env: str = "dev"
    database_url: str = "sqlite:///./todo.db"
    jwt_secret_key: str = "change_me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    cors_origins: list[str] = ["http://127.0.0.1:5173", "http://localhost:5173"]
    cors_origin_regex: str = r"https?://(127\.0\.0\.1|localhost)(:\d+)?"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value):
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


settings = Settings()
