from logging import Logger
from typing import Callable

from fastapi import FastAPI

from src.kernel.fastapi.settings.app import AppSettings
from src.kernel.rmq.connection_getter import get_connector
from src.kernel.rmq.migrations.queue import BaseQueueMigrator


def queue_declarer(app_settings: AppSettings, json_logger: Logger) -> Callable:
    async def _inner() -> None:
        rmq_connector = get_connector(app_settings)
        queue_migrator = BaseQueueMigrator(rmq_connector)
        queues = app_settings.RMQ_RUN_SETTINGS.queues

        for _, queue in queues.items():
            await queue_migrator.migrate(queue)
            json_logger.info(f"Declare queue: {queue.name}")

    return _inner


def register_rmq_queue_declare_handler(
    application: FastAPI, app_settings: AppSettings, json_logger: Logger
) -> None:
    application.add_event_handler("startup", queue_declarer(app_settings, json_logger))
