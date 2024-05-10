from typing import Callable, Type

from asyncio_connection_pool import ConnectionPool
from asyncpg.pool import Pool
from fastapi import Depends
from starlette.requests import Request

from src.kernel.database.postgres.i_repository import IRepository


def _get_db_pool(request: Request) -> Pool:
    return request.app.state.pool.postgres


def get_repository(
    repo_type: Type[IRepository],
) -> Callable[[ConnectionPool], IRepository]:
    def _get_repo(
        conn: ConnectionPool = Depends(_get_db_pool),
    ) -> IRepository:
        return repo_type(conn)

    return _get_repo
