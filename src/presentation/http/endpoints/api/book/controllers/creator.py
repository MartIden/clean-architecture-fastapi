from fastapi import Depends

from src.application.book.cases.book_crud import BookCrudCase
from src.domain.book.dto.new_book import NewBook
from src.domain.book.dto.request import NewBookRequest
from src.domain.book.dto.response import BookJsonResponse, BookOut
from src.domain.book.entity.book import Book
from src.kernel.fastapi.controller import IJsonController
from src.presentation.http.endpoints.api.book.depends.book_crud_case import get_book_crud_case


class BookCreatorController(IJsonController):

    def __init__(
        self,
        request: NewBookRequest,
        crud_case: BookCrudCase = Depends(get_book_crud_case)
    ):
        self.__request = request
        self.__crud_case = crud_case

    async def __create_book(self, request: NewBookRequest) -> Book:
        return await self.__crud_case.create(NewBook(**request.model_dump()))

    @staticmethod
    def __create_answer(book: Book) -> BookJsonResponse:
        return BookJsonResponse(success=True, answer=BookOut(**book.model_dump()))

    async def answer(self) -> BookJsonResponse:
        book = await self.__create_book(self.__request)
        return self.__create_answer(book)
