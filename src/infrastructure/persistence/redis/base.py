from typing import Any

import redis
from pydantic import BaseModel

from src.domain.common.ports.redis_repo import IRedisRepoPort


class BaseRedisRepo(IRedisRepoPort):

    def __init__(self, pool: redis.Redis):
        self._pool = pool

    async def add_model(self, key: str, model: BaseModel) -> int:
        return await self._pool.rpush(key, *[model.model_dump_json()])
    
    async def ping(self):
        return await self._pool.ping()

    async def get(self, key: str) -> Any:
        return await self._pool.get(key)

    async def get_list(self, key: str, start=0, end=1) -> Any:
        return await self._pool.lrange(key, start, end)

    async def delete(self, key: str):
        return await self._pool.delete(key)