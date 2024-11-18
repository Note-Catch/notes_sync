from os import environ

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class DefaultSettings(BaseSettings):
    ENV: str = environ.get("ENV", "local")
    PATH_PREFIX: str = environ.get("PATH_PREFIX", "/api/v1")
    API_HOST: str = environ.get("API_HOST", "0.0.0.0")
    API_PORT: int = int(environ.get("API_PORT", 8080))

    LOGSEQUENCE_CONSUMER_HOST: str = environ.get("LOGSEQUENCE_CONSUMER_HOST", API_HOST)
    LOGSEQUENCE_CONSUMER_PORT: int = int(environ.get("LOGSEQUENCE_CONSUMER_PORT", 8081))

    DB_NAME: str = environ.get("DB_NAME", "notes_sync_db")
    DB_PATH: str = environ.get("DB_PATH", "localhost")
    DB_USER: str = environ.get("DB_USER", "notes_sync_admin")
    DB_PORT: int = int(environ.get("DB_PORT", 5432))
    DB_PASSWORD: str = environ.get("DB_PASSWORD", "notes_sync_admin_pass")
    DB_POOL_SIZE: int = int(environ.get("DB_POOL_SIZE", 15))
    DB_CONNECT_RETRY: int = int(environ.get("DB_CONNECT_RETRY", 20))

    KAFKA_HOST: str = environ.get("KAFKA_HOST", "notes_sync_broker")
    KAFKA_PORT: int = int(environ.get("KAFKA_PORT", 29092))

    ADMIN_LOGIN: str = environ.get("ADMIN_LOGIN", "eoanermine")
    ADMIN_PASSWORD: str = environ.get("ADMIN_PASSWORD", "eoanermine")

    @property
    def database_settings(self) -> dict:
        """
        Get all settings for connection with database.
        """
        return {
            "database": self.DB_NAME,
            "user": self.DB_USER,
            "password": self.DB_PASSWORD,
            "host": self.DB_PATH,
            "port": self.DB_PORT,
        }

    @property
    def database_uri(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    @property
    def broker_uri(self) -> str:
        """
        Get uri for connection with message broker
        """
        return f"{self.KAFKA_HOST}:{self.KAFKA_PORT}"
