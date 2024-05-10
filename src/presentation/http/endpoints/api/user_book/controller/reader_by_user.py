from fastapi import Depends

from src.application.book.cases.user_book_crud import UserBookCrudCase
from src.domain.book.dto.response_user_book import UserBookOut, UserBooksJsonResponse, UsersBooksWrapper
from src.domain.book.entity.user_book import UserBook
from src.domain.user.entity.user import User
from src.kernel.fastapi.controller import IJsonController
from src.presentation.http.endpoints.api.book.depends.user_book_crud_case import get_user_book_crud_case
from src.presentation.http.endpoints.api.user.depends.user_by_token import get_user_by_token


class UserBookReaderByUserController(IJsonController):

    def __init__(
        self,
        user: User = Depends(get_user_by_token),
        crud_case: UserBookCrudCase = Depends(get_user_book_crud_case),
    ):
        self.__user = user
        self.__crud_case = crud_case

    async def __read_user_books_by_user_id(self, user_id: id) -> list[UserBook]:
        return await self.__crud_case.get_by_user_id(user_id)

    async def __count_by_user_id(self, user_id: int) -> int:
        return await self.__crud_case.count_by_user_id(user_id)

    @staticmethod
    def __create_answer(user_books: list[UserBook], count: int) -> UserBooksJsonResponse:
        entities = [UserBookOut(**user_book.model_dump())for user_book in user_books]

        return UserBooksJsonResponse(
            success=True,
            answer=UsersBooksWrapper(
                entities=entities,
                count=count
            )
        )

    async def answer(self) -> UserBooksJsonResponse:
        count = await self.__count_by_user_id(self.__user.id)
        books = await self.__read_user_books_by_user_id(self.__user.id)

        return self.__create_answer(books, count)
