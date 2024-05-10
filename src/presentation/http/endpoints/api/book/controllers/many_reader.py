from fastapi import Depends
from pypika import Order

from src.application.book.cases.book_crud import BookCrudCase
from src.domain.book.dto.response import BookOut, BooksJsonResponse, BooksWrapper
from src.domain.book.entity.book import Book
from src.kernel.fastapi.controller import IJsonController
from src.presentation.http.depends.order import get_order
from src.presentation.http.endpoints.api.book.depends.book_crud_case import get_book_crud_case


class BookReaderManyController(IJsonController):

    def __init__(
        self,
        limit: int,
        offset: int,
        order: Order = Depends(get_order),
        crud_case: BookCrudCase = Depends(get_book_crud_case)
    ):
        self.__limit = limit
        self.__offset = offset
        self.__order = order
        self.__crud_case = crud_case

    async def __count_books(self) -> int:
        return await self.__crud_case.count()

    async def __read_many_books(self, limit: int, offset: int, order: Order) -> list[Book]:
        return await self.__crud_case.read_all(limit, offset, order)

    @staticmethod
    def __create_answer(books: list[Book], count: int) -> BooksJsonResponse:
        entities = [BookOut(**book.model_dump()) for book in books]

        return BooksJsonResponse(
            success=True,
            answer=BooksWrapper(
                entities=entities,
                count=count
            )
        )

    async def answer(self) -> BooksJsonResponse:
        count = await self.__count_books()
        books = await self.__read_many_books(self.__limit, self.__offset, self.__order)
        return self.__create_answer(books, count)
