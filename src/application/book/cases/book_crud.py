from pydantic import BaseModel
from pypika import Order

from src.domain.book.dto.new_book import NewBook
from src.domain.book.dto.update_book import UpdateBook
from src.domain.book.entity.book import Book
from src.domain.book.exceptions.book_not_exists import BookIsNotExistsError
from src.domain.book.book.book_repo import IBookRepoPort


class BookCrudCase:

    def __init__(self, repo: IBookRepoPort):
        self.__repo = repo

    @staticmethod
    def __raise_if_not_exist(book: Book | BaseModel) -> None:
        if not book:
            raise BookIsNotExistsError("Book With Current Id Is Not Exist")
    
    async def create(self, schema: NewBook) -> Book:
        book = await self.__repo.create(schema)
        self.__raise_if_not_exist(book)
        return book

    async def read(self, row_id: int) -> Book | None:
        book = await self.__repo.read(row_id)
        self.__raise_if_not_exist(book)
        return book

    async def update(self, schema: UpdateBook) -> Book:
        book = await self.__repo.update(schema)
        self.__raise_if_not_exist(book)
        return book

    async def delete(self, row_id: int) -> Book | BaseModel | None:
        book = await self.__repo.delete(row_id)
        self.__raise_if_not_exist(book)
        return book

    async def read_all(self, limit: int, offset: int, order: Order) -> list[Book | BaseModel]:
        return await self.__repo.read_all(limit, offset, order)

    async def read_by_user(self, user_id: int) -> list[Book]:
        return await self.__repo.read_by_user(user_id)

    async def count(self) -> int:
        return await self.__repo.count()
