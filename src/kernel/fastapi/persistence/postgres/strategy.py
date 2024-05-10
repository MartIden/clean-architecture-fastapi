import asyncpg
from asyncio_connection_pool import ConnectionStrategy
from asyncpg import Connection

from src.kernel.fastapi.settings.app import AppSettings


class PostgresStrategy(ConnectionStrategy):

    def __init__(self, settings: AppSettings):
        self.__settings = settings

    @property
    def host(self) -> str:
        return self.__settings.POSTGRES_HOST

    @property
    def port(self) -> str:
        return self.__settings.POSTGRES_PORT

    @property
    def db_name(self) -> str:
        return self.__settings.POSTGRES_DB

    @property
    def schema(self) -> str:
        return self.__settings.POSTGRES_DB_SCHEMA

    @property
    def user(self) -> str:
        return self.__settings.POSTGRES_USER

    @property
    def password(self) -> str:
        return self.__settings.POSTGRES_PASSWORD

    async def make_connection(self) -> Connection:
        return await asyncpg.connect(
            host=self.host,
            port=self.port,
            database=self.db_name,
            user=self.user,
            password=self.password,
            server_settings={"search_path": self.schema}
        )

    def connection_is_closed(self, conn: Connection) -> bool:
        return conn.is_closed()

    async def close_connection(self, conn: Connection) -> None:
        await conn.close()
