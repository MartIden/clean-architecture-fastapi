from functools import lru_cache
from typing import Dict, Type

from src.kernel.fastapi.settings.app import AppSettings
from src.kernel.fastapi.settings.base import AppEnvTypes, BaseAppSettings
from src.kernel.fastapi.settings.dev import DevAppSettings
from src.kernel.fastapi.settings.prod import ProdAppSettings
from src.kernel.fastapi.settings.test import TestAppSettings

environments: Dict[AppEnvTypes, Type[AppSettings]] = {
    AppEnvTypes.DEV: DevAppSettings,
    AppEnvTypes.PROD: ProdAppSettings,
    AppEnvTypes.TEST: TestAppSettings,
}


@lru_cache
def get_app_settings() -> AppSettings:
    app_env = BaseAppSettings().app_env
    config = environments[app_env]
    return config()
