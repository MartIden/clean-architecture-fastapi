from fastapi import Depends

from src.domain.user.dto.request import UpdateUserRequest
from src.domain.user.dto.update_user import UpdateUser
from src.application.user.cases.crud import UserCrudCase
from src.domain.user.dto.response import UserJsonResponse, UserOut
from src.domain.user.entity.user import User
from src.application.user.cases.password import UserPasswordService
from src.kernel.fastapi.config import get_app_settings
from src.kernel.fastapi.controller import IJsonController
from src.kernel.fastapi.settings.app import AppSettings
from src.presentation.http.endpoints.api.user.depends.crud_case import get_crud_case
from src.presentation.http.endpoints.api.user.depends.password_service import get_password_service
from src.presentation.http.endpoints.api.user.depends.user_by_token import get_user_by_token


class UserUpdaterController(IJsonController):

    def __init__(
        self,
        request: UpdateUserRequest,
        app_settings: AppSettings = Depends(get_app_settings),
        password_service: UserPasswordService = Depends(get_password_service),
        crud_case: UserCrudCase = Depends(get_crud_case),
        _=Depends(get_user_by_token)
    ):
        self.__request = request
        self.__crud_case = crud_case
        self.__app_settings = app_settings
        self.__password_service = password_service

    @property
    def __password_hash(self) -> str | None:
        if not self.__request.password:
            return
        return self.__password_service.create_password(self.__request.password, self.__app_settings.SALT)

    async def __update(self, request: UpdateUserRequest, hashed_pass: str) -> User | None:
        user = UpdateUser(id=request.id, login=request.login, email=request.email, password=hashed_pass)
        return await self.__crud_case.update(user)

    @staticmethod
    def __create_answer(user: User) -> UserJsonResponse:
        return UserJsonResponse(success=True, answer=UserOut(**user.model_dump()))

    async def answer(self) -> UserJsonResponse:
        user = await self.__update(self.__request, self.__password_hash)
        return self.__create_answer(user)
