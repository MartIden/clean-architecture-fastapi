

import datetime

from pydantic import BaseModel
from pypika import PostgreSQLQuery, Table, JoinType

from src.domain.user.dto.new_user import NewUser
from src.domain.user.dto.update_user import UpdateUser
from src.domain.user.entity.user import User
from src.domain.user.exceptions.user import UserIsNotExists
from src.ports.user.user_repo import IUserRepoPort


class UserRepo(IUserRepoPort):

    _schema = User

    @property
    def table_name(self) -> str:
        return "users"

    async def create(self, schema: NewUser) -> User:
        now = int(datetime.datetime.now().timestamp())
        query = PostgreSQLQuery \
            .into(self.table) \
            .columns(
                self.table.login,
                self.table.password,
                self.table.email,
                self.table.created_at,
                self.table.updated_at,
            ) \
            .insert(
                schema.login,
                schema.password,
                schema.email,
                now,
                now,
            ) \
            .returning("*") \
            .get_sql()

        rows = await self._fetch_sql(query)
        if len(rows) > 0:
            return self._create_schema(rows[0], User)

    async def update(self, schema: UpdateUser) -> User | BaseModel | None:
        user = await self.read(schema.id)

        if not user:
            raise UserIsNotExists(f"User With Id {schema.id} Is Not Exist")

        query = PostgreSQLQuery.update(self.table) \
            .set(self.table.login, schema.login or user.login) \
            .set(self.table.password, schema.password or user.password) \
            .set(self.table.email, schema.email or user.email) \
            .set(self.table.updated_at, int(datetime.datetime.now().timestamp())) \
            .where(self.table.id == schema.id) \
            .get_sql()

        await self._fetch_sql(query)
        return await self.read(schema.id)

    async def read_by_login(self, login: str, password: str) -> User | None:
        query = self.from_table.select("*").where(
            (self.table.login == login) and (self.table.password == password)
        ).get_sql()

        rows = await self._fetch_sql(query)

        if len(rows) > 0:
            return self._create_schema(rows[0], self._schema)

    async def read_by_token(self, token: str) -> User | None:
        token_table = Table("tokens")

        query = self.from_table \
            .select(
                self.table.id,
                self.table.login,
                self.table.password,
                self.table.email,
                self.table.created_at,
                self.table.updated_at,
            ) \
            .join(token_table, JoinType.left) \
            .on(self.table.id == token_table.user_id) \
            .where(token_table.access_token == token)\
            .get_sql()

        rows = await self._fetch_sql(query)

        if len(rows) > 0:
            return self._create_schema(rows[0], self._schema)
