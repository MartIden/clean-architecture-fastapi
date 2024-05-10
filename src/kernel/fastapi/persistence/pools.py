from logging import Logger
from typing import Optional

from asyncio_connection_pool import ConnectionPool
from fastapi import FastAPI

from src.kernel.fastapi.settings.app import AppSettings


class DatabasePools:
    clickhouse: Optional[ConnectionPool] = None
    postgres: Optional[ConnectionPool] = None
    redis = None


def register_init_pools_handler(
    application: FastAPI, settings: AppSettings, json_logger: Logger
) -> None:  # noqa
    application.state.pool = DatabasePools()
