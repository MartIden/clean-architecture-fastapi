from logging import Logger

from fastapi import FastAPI

from src.kernel.fastapi.persistence.redis.pool_creator import create_redis
from src.kernel.fastapi.settings.app import AppSettings


def register_redis_handler(
    application: FastAPI, app_settings: AppSettings, json_logger: Logger
) -> None:
    application.add_event_handler("startup", create_redis(application, app_settings))
