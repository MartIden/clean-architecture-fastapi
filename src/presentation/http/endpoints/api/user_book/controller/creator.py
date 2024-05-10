from fastapi import Depends

from src.application.book.cases.user_book_crud import UserBookCrudCase
from src.domain.book.dto.new_user_book import NewUserBook
from src.domain.book.dto.request_user_book import NewUserBookRequest
from src.domain.book.dto.response_user_book import UserBookJsonResponse, UserBookOut
from src.domain.book.entity.user_book import UserBook
from src.domain.user.entity.user import User
from src.kernel.fastapi.controller import IJsonController
from src.presentation.http.endpoints.api.book.depends.user_book_crud_case import get_user_book_crud_case
from src.presentation.http.endpoints.api.user.depends.user_by_token import get_user_by_token


class UserBookCreatorController(IJsonController):

    def __init__(
        self,
        request: NewUserBookRequest,
        crud_case: UserBookCrudCase = Depends(get_user_book_crud_case),
        user: User = Depends(get_user_by_token)
    ):
        self.__request = request
        self.__crud_case = crud_case
        self.__user = user

    async def __create_user_book(self, request: NewUserBookRequest) -> UserBook:
        return await self.__crud_case.create(
            NewUserBook(user_id=self.__user.id, **request.model_dump())
        )

    @staticmethod
    def __create_answer(book: UserBook) -> UserBookJsonResponse:
        return UserBookJsonResponse(success=True, answer=UserBookOut(**book.model_dump()))

    async def answer(self) -> UserBookJsonResponse:
        book = await self.__create_user_book(self.__request)
        return self.__create_answer(book)
