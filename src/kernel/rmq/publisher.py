import traceback
from abc import ABC, abstractmethod
from logging import INFO
from typing import Any, Optional

from aio_pika import Message
from aio_pika.abc import DeliveryMode
from pydantic import BaseModel

from src.kernel.fastapi.settings.app import AppSettings
from src.kernel.logging.json_logger_getter import get_json_logger
from src.kernel.rmq.connector import BaseRMQConnector


class AbstractRMQPublisher(ABC):
    def __init__(self, connector: BaseRMQConnector, app_settings: AppSettings):
        self._connector = connector
        self._app_settings = app_settings
        self._logger = get_json_logger()

    @property
    def publisher_class(self) -> str:
        return type(self).__name__

    @property
    @abstractmethod
    def _exchange_name(self) -> Optional[str]:
        pass

    @abstractmethod
    async def publish(self, message: str) -> Any:
        pass

    @abstractmethod
    async def publish_model(self, message: BaseModel) -> Any:
        pass

    @abstractmethod
    async def _publish(self, message: bytes, **kwargs) -> Any:
        pass

    def _log_publisher(
        self,
        *,
        message: Optional[str] = None,
        extra: Optional[dict] = None,
        log_level=INFO,
    ):
        extra["publisher"] = self.publisher_class
        self._logger.log(log_level, message, extra)


class BaseRMQPublisher(AbstractRMQPublisher, ABC):
    async def _publish(self, message: bytes, **kwargs) -> Any:
        message = Message(message, delivery_mode=DeliveryMode.PERSISTENT)

        async with self._connector.channel_pool.acquire() as channel:
            exchange = await channel.get_exchange(self._exchange_name)
            return await exchange.publish(message, routing_key=self._exchange_name)

    def _log_message(self, message: str) -> None:
        self._log_publisher(
            message=f"Message to '{self._exchange_name}' has been sending",
            extra={"incoming_message": message},
        )

    def _log_err_message(self, message: str, exc: Exception):
        trace = traceback.format_tb(exc.__traceback__)
        extra = {"traceback": trace, "incoming_message": message}
        message = f"Message was not sent to '{self._exchange_name}' due to an error: '{str(exc)}'"
        self._log_publisher(message=message, extra=extra)

    async def publish(self, message: str) -> Any:
        try:
            bytes_message = message.encode("utf-8")
            publish_status = await self._publish(bytes_message)
            self._log_message(message)

            return publish_status
        except Exception as exc:
            self._log_err_message(message, exc)

    async def publish_model(self, message: BaseModel) -> Any:
        bytes_message = message.json().encode("utf-8")
        return await self._publish(bytes_message)
