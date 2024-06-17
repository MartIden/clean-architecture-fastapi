import datetime

from pydantic import BaseModel
from pypika import PostgreSQLQuery
from pypika.functions import Count

from src.domain.book.dto.new_user_book import NewUserBook
from src.domain.book.dto.update_user_book import UpdateUserBook
from src.domain.book.entity.user_book import UserBook
from src.domain.book.exceptions.user_book_not_exists import UserBookIsNotExists
from src.domain.book.book.user_book_repo import IUserBookRepoPort


class UserBookRepo(IUserBookRepoPort):

    _schema = UserBook

    @property
    def table_name(self) -> str:
        return "users_books"

    async def create(self, schema: NewUserBook) -> UserBook:
        now = int(datetime.datetime.now().timestamp())
        query = PostgreSQLQuery \
            .into(self.table) \
            .columns(
                self.table.user_id,
                self.table.book_id,
                self.table.created_at,
                self.table.updated_at,
            ) \
            .insert(
                schema.user_id,
                schema.book_id,
                now,
                now,
            ) \
            .returning("*") \
            .get_sql()

        rows = await self._fetch_sql(query)
        if len(rows) > 0:
            return self._create_schema(rows[0], UserBook)

    async def update(self, schema: UpdateUserBook) -> UserBook | BaseModel | None:
        user_book = await self.read(schema.id)

        if not user_book:
            raise UserBookIsNotExists("UserBook With Current Id Is Not Exist")

        query = PostgreSQLQuery.update(self.table) \
            .set(self.table.user_id, schema.user_id or UserBook.user_id) \
            .set(self.table.book_id, schema.book_id or UserBook.book_id) \
            .set(self.table.created_at, schema.created_at or UserBook.created_at) \
            .set(self.table.updated_at, int(datetime.datetime.now().timestamp())) \
            .where(self.table.id == schema.id) \
            .get_sql()

        await self._fetch_sql(query)
        return await self.read(schema.id)

    async def get_by_user_id(self, user_id: int) -> list[UserBook]:
        query = self.from_table.select("*").where(self.table.user_id == user_id).get_sql()

        rows = await self._fetch_sql(query)
        return self._create_schemas(rows, self._schema)

    async def count_by_user_id(self, user_id: int) -> int:
        query = self.from_table.select(Count("*")).where(self.table.user_id == user_id).get_sql()

        rows = await self._fetch_sql(query)

        if len(rows) > 0:
            return rows[0]["count"]
