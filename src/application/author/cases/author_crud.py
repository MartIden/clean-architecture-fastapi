from pydantic import BaseModel
from pypika import Order

from src.domain.author.dto.new_author import NewAuthor
from src.domain.author.dto.update_author import UpdateAuthor
from src.domain.author.entity.author import Author
from src.domain.author.exceptions.author_not_exists import AuthorIsNotExists
from src.ports.author.author_repo import IAuthorRepoPort


class AuthorCrudCase:

    def __init__(self, repo: IAuthorRepoPort):
        self.__repo = repo

    @staticmethod
    def __raise_if_not_exist(author: Author | BaseModel) -> None:
        if not author:
            raise AuthorIsNotExists("Author With Current Id Is Not Exist")

    async def create(self, schema: NewAuthor) -> Author:
        author = await self.__repo.create(schema)
        self.__raise_if_not_exist(author)
        return author

    async def read(self, row_id: int) -> Author | BaseModel | None:
        author = await self.__repo.read(row_id)
        self.__raise_if_not_exist(author)
        return author

    async def update(self, schema: UpdateAuthor) -> Author:
        author = await self.__repo.update(schema)
        self.__raise_if_not_exist(author)
        return author

    async def delete(self, row_id: int) -> Author | BaseModel | None:
        author = await self.__repo.delete(row_id)
        self.__raise_if_not_exist(author)
        return author

    async def read_all(self, limit: int, offset: int, order: Order) -> list[Author | BaseModel]:
        return await self.__repo.read_all(limit, offset, order)

    async def count(self) -> int:
        return await self.__repo.count()
