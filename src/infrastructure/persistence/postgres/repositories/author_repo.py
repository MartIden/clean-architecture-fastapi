import datetime

from pydantic import BaseModel
from pypika import PostgreSQLQuery

from src.domain.author.dto.new_author import NewAuthor
from src.domain.author.dto.update_author import UpdateAuthor
from src.domain.author.entity.author import Author
from src.domain.author.exceptions.author_not_exists import AuthorIsNotExists
from src.domain.author.ports.author_repo import IAuthorRepoPort


class AuthorRepo(IAuthorRepoPort):

    _schema = Author

    @property
    def table_name(self) -> str:
        return "authors"

    async def create(self, schema: NewAuthor) -> Author:
        now = int(datetime.datetime.now().timestamp())
        query = PostgreSQLQuery \
            .into(self.table) \
            .columns(
                self.table.name,
                self.table.surname,
                self.table.created_at,
                self.table.updated_at,
            ) \
            .insert(
                schema.name,
                schema.surname,
                now,
                now,
            ) \
            .returning("*") \
            .get_sql()

        rows = await self._fetch_sql(query)

        if len(rows) > 0:
            return self._create_schema(rows[0], self._schema)

    async def update(self, schema: UpdateAuthor) -> Author | BaseModel | None:
        author = await self.read(schema.id)

        if not author:
            raise AuthorIsNotExists("Author With Current Id Is Not Exist")

        query = PostgreSQLQuery.update(self.table) \
            .set(self.table.name, schema.name or author.name) \
            .set(self.table.surname, schema.surname or author.surname) \
            .set(self.table.updated_at, int(datetime.datetime.now().timestamp())) \
            .where(self.table.id == schema.id) \
            .get_sql()

        await self._fetch_sql(query)
        return await self.read(schema.id)
