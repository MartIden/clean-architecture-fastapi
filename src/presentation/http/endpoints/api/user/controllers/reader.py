from fastapi import Depends

from src.application.user.cases.crud import UserCrudCase
from src.domain.user.dto.response import UserJsonResponse, UserOut
from src.domain.user.entity.user import User
from src.kernel.fastapi.controller import IJsonController
from src.presentation.http.endpoints.api.user.depends.crud_case import get_crud_case


class UserReaderController(IJsonController):

    def __init__(
        self,
        row_id: int,
        crud_case: UserCrudCase = Depends(get_crud_case)
    ):
        self.__row_id = row_id
        self.__crud_case = crud_case

    async def __read(self, row_id: int) -> User:
        return await self.__crud_case.read(row_id)

    @staticmethod
    def __create_answer(user: User) -> UserJsonResponse:
        return UserJsonResponse(success=True, answer=UserOut(**user.model_dump()))

    async def answer(self) -> UserJsonResponse:
        user = await self.__read(self.__row_id)
        return self.__create_answer(user)
