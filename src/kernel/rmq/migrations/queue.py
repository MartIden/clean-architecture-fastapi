from abc import ABC, abstractmethod

from src.kernel.rmq.connector import BaseRMQConnector
from src.kernel.rmq.models import RmqQueue


class AbstractQueueMigrator(ABC):
    @abstractmethod
    async def migrate(self, queue: RmqQueue) -> None:
        pass


class BaseQueueMigrator(AbstractQueueMigrator):
    def __init__(self, connector: BaseRMQConnector):
        self._connector = connector

    async def __create_queue(self, queue: RmqQueue) -> None:
        async with self._connector.channel_pool.acquire() as channel:
            await channel.declare_queue(queue.name, **queue.kwargs)

    async def migrate(self, queue: RmqQueue) -> None:
        await self.__create_queue(queue)
