import datetime

from pydantic import BaseModel
from pypika import PostgreSQLQuery, Table, JoinType

from src.domain.book.dto.new_book import NewBook
from src.domain.book.dto.update_book import UpdateBook
from src.domain.book.entity.book import Book
from src.domain.book.exceptions.book_not_exists import BookIsNotExists
from src.domain.book.book.book_repo import IBookRepoPort


class BookRepo(IBookRepoPort):

    _schema = Book

    @property
    def table_name(self) -> str:
        return "books"

    async def create(self, schema: NewBook) -> Book | BaseModel:
        now = int(datetime.datetime.now().timestamp())
        query = PostgreSQLQuery \
            .into(self.table) \
            .columns(
                self.table.title,
                self.table.description,
                self.table.isbn,
                self.table.author_id,
                self.table.created_at,
                self.table.updated_at,
            ) \
            .insert(
                schema.title,
                schema.description,
                schema.isbn,
                schema.author_id,
                now,
                now,
            ) \
            .returning("*") \
            .get_sql()

        rows = await self._fetch_sql(query)

        if len(rows) > 0:
            return self._create_schema(rows[0], self._schema)

    async def update(self, schema: UpdateBook) -> Book | BaseModel | None:
        book = await self.read(schema.id)

        if not book:
            raise BookIsNotExists("Book With Current Id Is Not Exist")

        query = PostgreSQLQuery.update(self.table) \
            .set(self.table.title, schema.title or book.title) \
            .set(self.table.description, schema.description or book.description) \
            .set(self.table.isbn, schema.isbn or book.isbn) \
            .set(self.table.author_id, schema.author_id or book.author_id) \
            .set(self.table.updated_at, int(datetime.datetime.now().timestamp())) \
            .where(self.table.id == schema.id) \
            .returning("*")\
            .get_sql()

        rows = await self._fetch_sql(query)

        if len(rows) > 0:
            return self._create_schema(rows[0], self._schema)

    async def read_by_user(self, user_id: int) -> list[Book | BaseModel]:
        user_books_table = Table("users_books")
        users_table = Table("users")

        query = self.from_table.select(
            self.table.id,
            self.table.isbn,
            self.table.title,
            self.table.description,
            self.table.author_id,
            self.table.created_at,
            self.table.updated_at,
        )\
            .join(user_books_table, JoinType.left) \
            .on(user_books_table.book_id == self.table.id)\
            .join(users_table.id == user_books_table.user_id)\
            .where(user_books_table.user_id == user_id).get_sql()

        rows = await self._fetch_sql(query)
        return self._create_schemas(rows, self._schema)
