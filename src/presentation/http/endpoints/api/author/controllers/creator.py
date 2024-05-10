from fastapi import Depends

from src.application.author.cases.author_crud import AuthorCrudCase
from src.domain.author.dto.new_author import NewAuthor
from src.domain.author.dto.request import NewAuthorRequest
from src.domain.author.dto.response import AuthorJsonResponse, AuthorOut
from src.domain.author.entity.author import Author
from src.kernel.fastapi.controller import IJsonController
from src.presentation.http.endpoints.api.author.depends.author_crud import get_author_crud


class AuthorCreatorController(IJsonController):

    def __init__(
        self,
        request: NewAuthorRequest,
        author_crud: AuthorCrudCase = Depends(get_author_crud)
    ):
        self.__request = request
        self.__author_crud = author_crud

    async def __create_author(self, request: NewAuthorRequest) -> Author:
        return await self.__author_crud.create(NewAuthor(**request.model_dump()))

    @staticmethod
    def __create_answer(author: Author) -> AuthorJsonResponse:
        return AuthorJsonResponse(
            success=True,
            answer=AuthorOut(**author.model_dump())
        )

    async def answer(self) -> AuthorJsonResponse:
        author = await self.__create_author(self.__request)
        return self.__create_answer(author)
