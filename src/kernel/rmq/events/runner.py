import asyncio
from asyncio import AbstractEventLoop
from logging import Logger
from typing import Callable, List, Type

from fastapi import Depends, FastAPI

from src.kernel.fastapi.settings.app import AppSettings
from src.kernel.rmq.connector import BaseRMQConnector
from src.kernel.rmq.consumer import AbstractRMQConsumer
from src.kernel.rmq.dependencies import get_rmq_connector
from src.presentation.amqp.consumers import rmq_consumers


def get_amqp_uri(settings: AppSettings) -> str:
    return f"amqp://{settings.RMQ_USER}:{settings.RMQ_PASSWORD}@{settings.RMQ_HOST}:{settings.RMQ_PORT}"


def create_rmq_connector(
    application: FastAPI, settings: AppSettings, loop: AbstractEventLoop
) -> BaseRMQConnector:
    application.rmq_connector = BaseRMQConnector(
        amqp_uri=get_amqp_uri(settings), loop=loop
    )
    return application.rmq_connector


async def rmq_runner(
    application: FastAPI,
    loop: AbstractEventLoop,
    settings: AppSettings,
    consumers: List[Type[AbstractRMQConsumer]],
    rmq_connector: BaseRMQConnector = Depends(get_rmq_connector),
) -> None:
    for consumer in consumers:
        rmq_consumer = consumer(application, rmq_connector, settings)
        await loop.create_task(rmq_consumer.consume())


def init_rmq_on_startup(application: FastAPI, app_settings: AppSettings) -> Callable:
    async def init_rmq() -> None:
        loop = asyncio.get_running_loop()
        rmq_connector = create_rmq_connector(application, app_settings, loop)
        await rmq_runner(application, loop, app_settings, rmq_consumers, rmq_connector)

    return init_rmq


def register_rmq_handler(
    application: FastAPI, app_settings: AppSettings, json_logger: Logger
) -> None:
    application.add_event_handler(
        "startup", init_rmq_on_startup(application, app_settings)
    )
