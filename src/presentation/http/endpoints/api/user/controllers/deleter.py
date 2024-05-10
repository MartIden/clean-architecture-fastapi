from fastapi import Depends

from src.application.user.cases.crud import UserCrudCase
from src.domain.user.dto.response import UserJsonResponse, UserOut
from src.domain.user.entity.user import User
from src.kernel.fastapi.controller import IJsonController
from src.presentation.http.endpoints.api.user.depends.crud_case import get_crud_case
from src.presentation.http.endpoints.api.user.depends.user_by_token import get_user_by_token


class UserDeleterController(IJsonController):

    def __init__(
        self,
        crud_case: UserCrudCase = Depends(get_crud_case),
        current_user: User = Depends(get_user_by_token)
    ):
        self.__crud_case = crud_case
        self.__current_user = current_user

    async def __delete(self, row_id: int) -> User:
        return await self.__crud_case.delete(row_id)

    @staticmethod
    def __create_answer(user: User) -> UserJsonResponse:
        return UserJsonResponse(success=True, answer=UserOut(**user.model_dump()))

    async def answer(self) -> UserJsonResponse:
        user = await self.__delete(self.__current_user.id)
        return self.__create_answer(user)
