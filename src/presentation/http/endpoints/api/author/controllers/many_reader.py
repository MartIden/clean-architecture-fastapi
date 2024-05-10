from fastapi import Depends
from pypika import Order

from src.application.author.cases.author_crud import AuthorCrudCase
from src.domain.author.dto.response import AuthorsWrapper, AuthorsJsonResponse, AuthorOut
from src.domain.author.entity.author import Author
from src.kernel.fastapi.controller import IJsonController
from src.presentation.http.depends.order import get_order
from src.presentation.http.endpoints.api.author.depends.author_crud import get_author_crud


class AuthorManyReaderController(IJsonController):

    def __init__(
        self,
        limit: int,
        offset: int,
        order: Order = Depends(get_order),
        author_crud: AuthorCrudCase = Depends(get_author_crud)
    ):
        self.__limit = limit
        self.__offset = offset
        self.__order = order
        self.__author_crud = author_crud

    async def __count_articles(self) -> int:
        return await self.__author_crud.count()

    async def __read_many_author(self, limit: int, offset: int, order: Order) -> list[Author]:
        return await self.__author_crud.read_all(limit, offset, order)

    @staticmethod
    def __create_answer(authors: list[Author], count: int) -> AuthorsJsonResponse:
        entities = [AuthorOut(**author.model_dump()) for author in authors]

        return AuthorsJsonResponse(
            success=True,
            answer=AuthorsWrapper(
                entities=entities,
                count=count
            )
        )

    async def answer(self) -> AuthorsJsonResponse:
        count = await self.__count_articles()
        authors = await self.__read_many_author(self.__limit, self.__offset, self.__order)
        return self.__create_answer(authors, count)
