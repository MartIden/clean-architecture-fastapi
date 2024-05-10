from fastapi import Depends

from src.application.user.cases.crud import UserCrudCase
from src.domain.user.dto.new_user import NewUser
from src.domain.user.dto.request import NewUserRequest
from src.domain.user.dto.response import UserJsonResponse, UserOut
from src.domain.user.entity.user import User
from src.application.user.cases.password import UserPasswordService
from src.kernel.fastapi.config import get_app_settings
from src.kernel.fastapi.controller import IJsonController
from src.kernel.fastapi.settings.app import AppSettings
from src.presentation.http.endpoints.api.user.depends.crud_case import get_crud_case
from src.presentation.http.endpoints.api.user.depends.password_service import get_password_service


class UserCreatorController(IJsonController):

    def __init__(
        self,
        request: NewUserRequest,
        app_settings: AppSettings = Depends(get_app_settings),
        password_service: UserPasswordService = Depends(get_password_service),
        crud_case: UserCrudCase = Depends(get_crud_case)
    ):
        self.__request = request
        self.__crud_case = crud_case
        self.__app_settings = app_settings
        self.__password_service = password_service

    @property
    def __salt(self) -> str:
        return self.__app_settings.SALT

    @property
    def __password(self) -> str:
        return self.__request.password

    def __create_password_hash(self, password: str, salt: str) -> str:
        return self.__password_service.create_password(password, salt)

    async def __create(self, request: NewUserRequest, hashed_pass: str) -> User | None:
        user = NewUser(login=request.login, email=request.email, password=hashed_pass)
        return await self.__crud_case.create(user)

    @staticmethod
    def __create_answer(user: User) -> UserJsonResponse:
        return UserJsonResponse(success=True, answer=UserOut(**user.model_dump()))

    async def answer(self) -> UserJsonResponse:
        password_hash = self.__create_password_hash(self.__password, self.__salt)
        user = await self.__create(self.__request, password_hash)
        return self.__create_answer(user)
