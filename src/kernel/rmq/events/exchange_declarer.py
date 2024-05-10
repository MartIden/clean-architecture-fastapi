from logging import Logger
from typing import Callable

from fastapi import FastAPI

from src.kernel.fastapi.settings.app import AppSettings
from src.kernel.rmq.connection_getter import get_connector
from src.kernel.rmq.migrations.exchanges import BaseExchangeMigrator


def exchange_declarer(app_settings: AppSettings, json_logger: Logger) -> Callable:
    async def _inner() -> None:
        rmq_connector = get_connector(app_settings)
        exchange_migrator = BaseExchangeMigrator(rmq_connector)
        exchanges = app_settings.RMQ_RUN_SETTINGS.exchanges

        for _, exchange in exchanges.items():
            await exchange_migrator.migrate(exchange)
            json_logger.info(f"Declare exchange: {exchange.name}")

    return _inner


def register_rmq_exchange_declare_handler(
    application: FastAPI, app_settings: AppSettings, json_logger: Logger
) -> None:
    application.add_event_handler(
        "startup", exchange_declarer(app_settings, json_logger)
    )
