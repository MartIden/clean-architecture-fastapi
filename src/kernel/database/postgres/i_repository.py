from abc import abstractmethod
from typing import Any, Optional, Type

from asyncio_connection_pool import ConnectionPool
from pydantic import BaseModel
from pypika import Table, Query, functions, Order


class IRepository:

    _schema: Type[BaseModel] = None

    def __init__(self, pool: ConnectionPool) -> None:
        self._pool = pool

    @property
    @abstractmethod
    def table_name(self) -> str:
        pass

    @property
    def table(self):
        return Table(self.table_name)

    @property
    def from_table(self):
        return Query.from_(self.table)

    @classmethod
    def _create_schema(cls, row: Any, schema_type: type[BaseModel]) -> BaseModel | Any:
        return schema_type(**row) if row else None

    @classmethod
    def _create_schemas(cls, rows: list[Any], schema_type: type[BaseModel]) -> list[BaseModel | Any]:
        schemas = [cls._create_schema(row, schema_type) for row in rows]
        return schemas

    @property
    def pool(self) -> ConnectionPool:
        return self._pool

    async def count(self) -> int:
        query = self.from_table.select(functions.Count("*")).get_sql()
        rows = await self._fetch_sql(query)
        return next((row.get("count") for row in rows), 0)

    async def delete(self, row_id: int) -> BaseModel | Any | None:
        row = await self.read(row_id)

        if not row:
            return

        query = self.from_table.delete().where(self.table.id == row_id).get_sql()
        await self._fetch_sql(query)

        return row

    async def read(self, row_id: int) -> BaseModel | Any:
        query = self.from_table.select("*").where(self.table.id == row_id).get_sql()
        rows = await self._fetch_sql(query)
        return next((self._create_schema(row, self._schema) for row in rows), 0)

    async def read_all(self, limit: int, offset: int, order: Order) -> list[BaseModel | Any]:
        query = self.from_table.select("*")[offset:limit].orderby("id", order=order).get_sql()
        rows = await self._fetch_sql(query)
        return self._create_schemas(rows, self._schema)

    async def _fetch_sql(self, query, **kwargs) -> Optional[Any]:
        async with self.pool.get_connection() as connection:
            async with connection.transaction():
                result = await connection.fetch(query, **kwargs)
                return result
