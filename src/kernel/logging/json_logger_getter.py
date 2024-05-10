import logging

from src.kernel.fastapi.config import get_app_settings
from src.kernel.fastapi.settings.app import AppSettings
from src.kernel.logging.json_logger import JsonLoggerFactory


def get_json_logger(
    name: str = "default", settings: AppSettings = get_app_settings()
) -> logging.Logger:
    return JsonLoggerFactory(name, settings).create()
