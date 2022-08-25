import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    POSTGRES_USER: Optional[str] = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: Optional[str] = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: Optional[str] = os.getenv("POSTGRES_DB")
    DATABASE_URL = (
        f"postgresql://{POSTGRES_USER}:"
        f"{POSTGRES_PASSWORD}@{POSTGRES_HOST}:"
        f"{POSTGRES_PORT}/{POSTGRES_DB}"
    )


settings = Settings()
