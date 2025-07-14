from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    DB_URL: str = "sqlite+aiosqlite:///./db.sqlite3"
    # DB_ECHO: bool = False
    DB_ECHO: bool = True


settings = Settings()
