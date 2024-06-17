from pydantic import BaseModel
from pypika import Order

from src.domain.book.dto.new_user_book import NewUserBook
from src.domain.book.dto.update_user_book import UpdateUserBook
from src.domain.book.entity.user_book import UserBook
from src.domain.book.exceptions.user_book_not_exists import UserBookIsNotExistsError
from src.domain.book.book.user_book_repo import IUserBookRepoPort

class UserBookCrudCase:

    def __init__(self, repo: IUserBookRepoPort):
        self.__repo = repo

    @staticmethod
    def __raise_if_not_exist(user_book: UserBook | BaseModel) -> None:
        if not user_book:
            raise UserBookIsNotExistsError("UserBook With Current Id Is Not Exist")
    
    async def create(self, schema: NewUserBook) -> UserBook:
        user_book = await self.__repo.create(schema)
        self.__raise_if_not_exist(user_book)
        return user_book

    async def get_by_user_id(self, user_id: int) -> list[UserBook]:
        return await self.__repo.get_by_user_id(user_id)

    async def count_by_user_id(self, user_id: int) -> int:
        return await self.__repo.count_by_user_id(user_id)

    async def read(self, row_id: int) -> UserBook | None:
        user_book = await self.__repo.read(row_id)
        self.__raise_if_not_exist(user_book)
        return user_book

    async def update(self, schema: UpdateUserBook) -> UserBook:
        user_book = await self.__repo.update(schema)
        self.__raise_if_not_exist(user_book)
        return user_book

    async def delete(self, row_id: int) -> UserBook | BaseModel | None:
        user_book = await self.__repo.delete(row_id)
        self.__raise_if_not_exist(user_book)
        return user_book

    async def read_all(self, limit: int, offset: int, order: Order) -> list[UserBook | BaseModel]:
        return await self.__repo.read_all(limit, offset, order)

    async def count(self) -> int:
        return await self.__repo.count()
