from asyncio import AbstractEventLoop
from typing import Optional

from aio_pika import Channel, connect_robust
from aio_pika.abc import AbstractRobustConnection
from aio_pika.pool import Pool

from src.domain.common.singletone import Singleton


class BaseRMQConnector(Singleton):

    def __init__(
        self, amqp_uri: str, loop: Optional[AbstractEventLoop] = None, pool_size=10
    ):
        self._url = amqp_uri
        self._loop = loop
        self._pool_size = pool_size

        self._connection_pool = self._set_connection_pool()
        self._channel_pool = self._set_channel_pool()

    @property
    def connection_pool(self) -> Pool[AbstractRobustConnection]:
        return self._connection_pool

    @property
    def channel_pool(self) -> Pool[Channel]:
        return self._channel_pool

    async def _get_connection(self) -> AbstractRobustConnection:
        return await connect_robust(self._url, pool=self._loop)

    async def _get_channel(self) -> Channel:
        async with self._connection_pool.acquire() as connection:
            return await connection.channel()

    def _set_connection_pool(self) -> Pool:
        return Pool(self._get_connection, max_size=self._pool_size)

    def _set_channel_pool(self) -> Pool:
        return Pool(self._get_channel, max_size=self._pool_size)
