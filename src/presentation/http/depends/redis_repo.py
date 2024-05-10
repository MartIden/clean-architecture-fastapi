from typing import Callable, Type

from fastapi import Depends
from starlette.requests import Request
import redis.asyncio as redis

from src.domain.common.ports.redis_repo import IRedisRepoPort


def _get_db_pool(request: Request) -> redis.Redis:
    return request.app.state.pool.redis


def get_redis_repository(
    repo_type: Type[IRedisRepoPort],
) -> Callable[[redis.Redis], IRedisRepoPort]:
    def _get_repo(
        pool: redis.Redis = Depends(_get_db_pool),
    ) -> IRedisRepoPort:
        return repo_type(pool)

    return _get_repo
