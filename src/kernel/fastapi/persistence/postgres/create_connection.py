from typing import Callable

from asyncio_connection_pool import ConnectionPool
from fastapi import FastAPI

from src.kernel.fastapi.persistence.postgres.strategy import PostgresStrategy
from src.kernel.fastapi.settings.app import AppSettings
from src.kernel.logging.json_logger_getter import get_json_logger


def run_postgres_db(
    app: FastAPI,
    settings: AppSettings,
) -> Callable:
    async def start_app() -> None:
        await create_db_pool(app, settings)

    return start_app


async def create_db_pool(app: FastAPI, settings: AppSettings) -> None:
    logger = get_json_logger()
    logger.info("Connecting to PostgreSQL")

    app.state.pool.postgres = ConnectionPool(
        strategy=PostgresStrategy(settings),
        max_size=settings.MAX_CONNECTION,
        burst_limit=round(1.3 * settings.MAX_CONNECTION),
    )

    logger.info("Connection to PostgreSQL established")
