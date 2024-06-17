import datetime

from pydantic import BaseModel
from pypika import PostgreSQLQuery

from src.domain.user.dto.token.new_token import NewToken
from src.domain.user.dto.token.update_token import UpdateToken
from src.domain.user.entity.token import Token
from src.domain.user.exceptions.token import TokenIsNotExistsError
from src.domain.user.user.token_repo import ITokenRepoPort


class TokenRepo(ITokenRepoPort):

    _schema = Token

    @property
    def table_name(self) -> str:
        return "tokens"

    async def create(self, schema: NewToken) -> Token:
        now = int(datetime.datetime.now().timestamp())
        expired_at = int((datetime.datetime.now() + datetime.timedelta(days=30)).timestamp())

        query = PostgreSQLQuery \
            .into(self.table) \
            .columns(
                self.table.access_token,
                self.table.is_active,
                self.table.user_id,
                self.table.expired_at,
                self.table.created_at,
                self.table.updated_at,
            ) \
            .insert(
                schema.access_token,
                schema.is_active,
                schema.user_id,
                expired_at,
                now,
                now,
            ) \
            .returning("*") \
            .get_sql()

        rows = await self._fetch_sql(query)
        if len(rows) > 0:
            return self._create_schema(rows[0], self._schema)

    async def update(self, schema: UpdateToken) -> Token | BaseModel | None:
        token = await self.read(schema.id)

        if not token:
            raise TokenIsNotExistsError("Token With Current Id Is Not Exist")

        query = PostgreSQLQuery.update(self.table) \
            .set(self.table.access_token, schema.access_token or token.access_token) \
            .set(self.table.is_active, schema.is_active or token.is_active) \
            .set(self.table.user_id, schema.user_id or token.user_id) \
            .set(self.table.created_at, schema.created_at or token.created_at) \
            .set(self.table.updated_at, int(datetime.datetime.now().timestamp())) \
            .where(self.table.id == schema.id) \
            .get_sql()

        await self._fetch_sql(query)
        return await self.read(schema.id)

    async def read_by_token(self, token: str) -> Token | None:
        query = self.from_table.select("*").where(self.table.access_token == token).get_sql()
        rows = await self._fetch_sql(query)
        return next((self._create_schema(row, self._schema) for row in rows), None)
