from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from src.kernel.fastapi.persistence.postgres.utils.configs import get_postgres_dsn
from src.kernel.fastapi.settings.base import BaseAppSettings
from src.kernel.rmq.models import RmqSettings


class AppSettings(BaseAppSettings):

    TEST: str

    DEBUG: bool = False
    DOCS_URL: str | None = None
    OPENAPI_PREFIX: str = ""
    OPENAPI_URL: Optional[str] = None
    REDOC_URL: str | None = None
    TITLE: str = "book-storage"
    VERSION: str = "0.0.1"
    ROOT_DIR: Path = Path(__file__).parent.parent.parent.parent.parent.resolve()
    ENV_FILE: str = f'{ROOT_DIR}/.env'

    """ DOC_AUTH """
    DOC_LOGIN: str = "admin"
    DOC_PASS: str = "s#d23x4&*d32"

    """POSTGRES SETTINGS"""
    POSTGRES_ENGINE: str = Field("postgresql", validation_alias="POSTGRES_ENGINE")
    POSTGRES_USER: str = Field(..., validation_alias="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., validation_alias="POSTGRES_PASSWORD")
    POSTGRES_HOST: str = Field(..., validation_alias="POSTGRES_HOST")
    POSTGRES_PORT: str = Field(..., validation_alias="POSTGRES_PORT")
    POSTGRES_DB: str = Field(..., validation_alias="POSTGRES_DB")
    POSTGRES_DB_SCHEMA: str = Field("public", validation_alias="POSTGRES_DB_SCHEMA")

    POSTGRES_DSN: str = Field(get_postgres_dsn(), validation_alias="POSTGRES_DSN")

    """ RMQ SETTINGS """
    RMQ_USER: str = Field("guest", env="RMQ_USER")
    RMQ_PASSWORD: str = Field("guest", env="RMQ_PASSWORD")
    RMQ_HOST: str = Field("127.0.0.1", env="RMQ_HOST")
    RMQ_PORT: str = Field("5672", env="RMQ_PORT")
    RMQ_RUN_SETTINGS: RmqSettings = Field(..., env="RMQ_RUN_SETTINGS")

    MAX_CONNECTION: int = 10
    SALT: str = "R6^,)7^$==sOT@hs0"
    SHOW_TRACEBACK_IN_RESPONSE: bool = Field(False, validation_alias="SHOW_TRACEBACK_IN_RESPONSE")

    ALLOWED_HOSTS: List[str] = [
        "*",
    ]

    LOGGING_LEVEL: int = Field(20, validation_alias="LOGGING_LEVEL")

    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding='utf-8')

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.DEBUG,
            "docs_url": self.DOCS_URL,
            "openapi_prefix": self.OPENAPI_PREFIX,
            "openapi_url": self.OPENAPI_URL,
            "redoc_url": self.REDOC_URL,
            "title": self.TITLE,
            "version": self.VERSION,
        }
