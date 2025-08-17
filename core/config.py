# ====== Configuration for SQLite Database ====== #
from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings


###### Building right path to DB ######
BASE_DIR = Path(__file__).parent.parent

DB_PATH = BASE_DIR / "db.sqlite3"


class DbSettings(BaseModel):
    URL: str = f"sqlite+aiosqlite:///{DB_PATH}"
    # ECHO: bool = False
    ECHO: bool = True


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15  # On dev it can be 3


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    DB: DbSettings = DbSettings()

    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
