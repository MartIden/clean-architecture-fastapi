from logging import Logger
from typing import Callable

from fastapi import FastAPI

from src.kernel.fastapi.settings.app import AppSettings
from src.kernel.rmq.connection_getter import get_connector
from src.kernel.rmq.migrations.binding import BaseRmqBinder


def get_binder(app_settings: AppSettings, json_logger: Logger) -> Callable:
    async def _inner() -> None:
        rmq_connector = get_connector(app_settings)
        binder = BaseRmqBinder(rmq_connector)
        bindings = app_settings.RMQ_RUN_SETTINGS.bindings

        for _, binding in bindings.items():
            await binder.declare(binding)
            logging_message = f"Declare binding from exchange {binding.exchange} to queue {binding.queue}"
            json_logger.info(logging_message)

    return _inner


def register_rmq_bind_handler(
    application: FastAPI, app_settings: AppSettings, json_logger: Logger
) -> None:
    application.add_event_handler("startup", get_binder(app_settings, json_logger))
