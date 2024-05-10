from enum import Enum
from typing import Union

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppEnvTypes(Enum):
    PROD: Union["AppEnvTypes", str] = "prod"
    DEV:  Union["AppEnvTypes", str] = "dev"
    TEST: Union["AppEnvTypes", str] = "test"


class BaseAppSettings(BaseSettings):
    app_env: AppEnvTypes = Field("Name of env to current application", validation_alias="APP_ENV")

    class Config:
        env_file = ".env"
