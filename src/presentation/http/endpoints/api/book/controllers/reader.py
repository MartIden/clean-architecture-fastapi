from fastapi import Depends

from src.application.book.cases.book_crud import BookCrudCase
from src.domain.book.dto.response import BookJsonResponse, BookOut
from src.domain.book.entity.book import Book
from src.kernel.fastapi.controller import IJsonController
from src.presentation.http.endpoints.api.book.depends.book_crud_case import get_book_crud_case


class BookReaderController(IJsonController):

    def __init__(
        self,
        row_id: int,
        crud_case: BookCrudCase = Depends(get_book_crud_case)
    ):
        self.__row_id = row_id
        self.__crud_case = crud_case

    async def __read_book(self, row_id: int) -> Book:
        return await self.__crud_case.read(row_id)

    @staticmethod
    def __create_answer(book: Book) -> BookJsonResponse:
        return BookJsonResponse(success=True, answer=BookOut(**book.model_dump()))

    async def answer(self) -> BookJsonResponse:
        book = await self.__read_book(self.__row_id)
        return self.__create_answer(book)
