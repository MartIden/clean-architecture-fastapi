from abc import ABC, abstractmethod

from src.kernel.rmq.connector import BaseRMQConnector
from src.kernel.rmq.models import RmqQueue, RmqExchange


class AbstractExchangeMigrator(ABC):
    @abstractmethod
    async def migrate(self, queue: RmqQueue) -> None:
        pass


class BaseExchangeMigrator(AbstractExchangeMigrator):

    def __init__(self, connector: BaseRMQConnector):
        self._connector = connector

    async def migrate(self, exchange: RmqExchange) -> None:
        async with self._connector.channel_pool.acquire() as channel:
            await channel.declare_exchange(
                exchange.name, exchange.exchange_type, **exchange.kwargs
            )
