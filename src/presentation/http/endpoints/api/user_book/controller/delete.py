from fastapi import Depends

from src.application.book.cases.user_book_crud import UserBookCrudCase
from src.domain.book.dto.response_user_book import UserBookJsonResponse, UserBookOut
from src.domain.book.entity.user_book import UserBook
from src.kernel.fastapi.controller import IJsonController
from src.presentation.http.endpoints.api.book.depends.user_book_crud_case import get_user_book_crud_case
from src.presentation.http.endpoints.api.user.depends.user_by_token import get_user_by_token


class UserBookDeleterController(IJsonController):

    def __init__(
        self,
        row_id: int,
        crud_case: UserBookCrudCase = Depends(get_user_book_crud_case),
        _=Depends(get_user_by_token)
    ):
        self.__row_id = row_id
        self.__crud_case = crud_case

    async def __read_user_book(self, row_id: id) -> UserBook:
        return await self.__crud_case.read(row_id)

    @staticmethod
    def __create_answer(book: UserBook) -> UserBookJsonResponse:
        return UserBookJsonResponse(success=True, answer=UserBookOut(**book.model_dump()))

    async def answer(self) -> UserBookJsonResponse:
        book = await self.__read_user_book(self.__row_id)
        return self.__create_answer(book)
