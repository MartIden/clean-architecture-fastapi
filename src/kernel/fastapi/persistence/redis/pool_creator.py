from typing import Callable

import redis.asyncio as redis
from fastapi import FastAPI

from src.kernel.fastapi.settings.app import AppSettings
from src.kernel.logging.json_logger_getter import get_json_logger


async def init_redis_pool(app: FastAPI, settings: AppSettings) -> None:
    logger = get_json_logger()
    logger.info("Connecting to Redis")

    app.state.pool.redis = await redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_INDEX,
        password=settings.REDIS_PASSWORD,
        ssl=settings.REDIS_SSL
    )

    logger.info("Connection to Redis established")


def create_redis(app: FastAPI, settings: AppSettings) -> Callable:
    async def wrap() -> None:
        await init_redis_pool(app, settings)
    return wrap
