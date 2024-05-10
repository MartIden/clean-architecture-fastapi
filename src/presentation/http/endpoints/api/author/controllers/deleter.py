from fastapi import Depends

from src.application.author.cases.author_crud import AuthorCrudCase
from src.domain.author.dto.response import AuthorJsonResponse, AuthorOut
from src.domain.author.entity.author import Author
from src.kernel.fastapi.controller import IJsonController
from src.presentation.http.endpoints.api.author.depends.author_crud import get_author_crud


class AuthorDeleterController(IJsonController):

    def __init__(
        self,
        row_id: int,
        author_crud: AuthorCrudCase = Depends(get_author_crud)
    ):
        self.__row_id = row_id
        self.__author_crud = author_crud

    async def __delete_author(self, row_id: int) -> Author:
        return await self.__author_crud.delete(row_id)

    @staticmethod
    def __create_answer(author: Author) -> AuthorJsonResponse:
        return AuthorJsonResponse(
            success=True,
            answer=AuthorOut(**author.model_dump())
        )

    async def answer(self) -> AuthorJsonResponse:
        author = await self.__delete_author(self.__row_id)
        return self.__create_answer(author)
