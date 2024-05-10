from fastapi import Depends

from src.application.user.cases.token_creator import TokenCreatorCase
from src.domain.user.dto.token.json_response import TokenJsonResponse, TokenOut
from src.domain.user.dto.token.new_token import NewTokenRequest
from src.domain.user.entity.token import Token
from src.kernel.fastapi.controller import IJsonController
from src.presentation.http.endpoints.api.user.depends.token_creator_case import get_token_creator_case


class TokenCreatorController(IJsonController):

    def __init__(
        self,
        request: NewTokenRequest,
        token_creator: TokenCreatorCase = Depends(get_token_creator_case)
    ):
        self.__request = request
        self.__token_creator = token_creator

    async def __create_token(self, login: str, password: str) -> Token | None:
        return await self.__token_creator.create_token(login, password)

    @staticmethod
    def __create_answer(token: Token) -> TokenJsonResponse:
        return TokenJsonResponse(success=True, answer=TokenOut(**token.model_dump()))

    async def answer(self) -> TokenJsonResponse:
        token = await self.__create_token(self.__request.login, self.__request.password)
        if not token:
            raise Exception("Failed To Create The Token")
        return self.__create_answer(token)
