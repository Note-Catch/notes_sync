from os import environ
from typing import Any, Dict

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class DefaultSettings(BaseSettings):
    ENV: str = environ.get("ENV", "local")
    APP_HOST: str = environ.get("APP_HOST", "0.0.0.0")
    APP_PORT: int = environ.get("APP_PORT", 8080)
