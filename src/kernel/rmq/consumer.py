from typing import List, Optional, Type
from abc import ABC, abstractmethod
import json

from aio_pika.abc import AbstractIncomingMessage
from fastapi import FastAPI

from src.kernel.fastapi.persistence.pools import DatabasePools
from src.kernel.fastapi.settings.app import AppSettings
from src.kernel.logging.json_logger_getter import get_json_logger
from src.kernel.rmq.connector import BaseRMQConnector
from src.kernel.rmq.exceptions import NackInterruptException, InterruptException
from src.kernel.rmq.handlers.factory_method import AbstractRmqHandlerCreator
from src.kernel.rmq.handlers.handlers_runner import HandlersRunner


class AbstractRMQConsumer(ABC):
    @abstractmethod
    async def consume(self, no_ack=False, **kwargs):
        pass


class BaseRMQConsumer(AbstractRMQConsumer):
    def __init__(
        self,
        application: FastAPI,
        connector: BaseRMQConnector,
        app_settings: AppSettings,
    ):
        self._connector = connector
        self._application = application
        self._app_settings = app_settings
        self._logger = get_json_logger()

    @property
    def _auto_ack(self) -> bool:
        return False

    @property
    def _connection_pools(self) -> DatabasePools:
        return self._application.state.pool

    @abstractmethod
    async def _message_handle(self, message: AbstractIncomingMessage):
        """Implement this method to handle incoming messages from consumer"""
        pass

    @property
    @abstractmethod
    def _queue_name(self) -> str:
        pass

    def _logging_message(self, message: str) -> None:
        consumer = type(self).__name__
        extra = {"consumer": consumer, "received_message": message}
        self._logger.info(f"{consumer}: Message received", extra=extra)

    def _message_to_dict(self, message: AbstractIncomingMessage) -> dict:
        body = message.body.decode()
        self._logging_message(body)
        return json.loads(body)

    async def _process_incoming_message(self, message: AbstractIncomingMessage) -> None:
        try:
            await self._message_handle(message)
            await message.ack()
        except NackInterruptException:
            await message.nack(requeue=False)
        except (InterruptException, Exception):
            if self._auto_ack:
                await message.ack()

    async def consume(self, no_ack=False, **kwargs):
        async with self._connector.channel_pool.acquire() as channel:
            queue = await channel.get_queue(self._queue_name)

            await queue.consume(self._process_incoming_message, no_ack=no_ack, **kwargs)
            self._logger.info(
                f"{type(self).__name__} for queue: '{self._queue_name}' has been launched"
            )


class BaseHandlersRunnerRMQConsumer(BaseRMQConsumer, ABC):

    _handlers_factories: Optional[List[Type[AbstractRmqHandlerCreator]]] = None

    async def _message_handle(self, message: AbstractIncomingMessage):
        try:
            message = self._message_to_dict(message)
            await HandlersRunner(
                message,
                self._handlers_factories,
                self._connector,
                self._connection_pools,
            ).run()
        except json.decoder.JSONDecodeError:
            self._logger.info("The message has an invalid JSON structure")
