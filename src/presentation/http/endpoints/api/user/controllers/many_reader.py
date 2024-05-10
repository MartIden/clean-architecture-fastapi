from fastapi import Depends
from pypika import Order

from src.application.user.cases.crud import UserCrudCase
from src.domain.user.dto.response import UserOut, UsersJsonResponse, UsersWrapper
from src.domain.user.entity.user import User
from src.kernel.fastapi.controller import IJsonController
from src.presentation.http.depends.order import get_order
from src.presentation.http.endpoints.api.user.depends.crud_case import get_crud_case


class UserManyReaderController(IJsonController):

    def __init__(
        self,
        limit: int,
        offset: int,
        order: Order = Depends(get_order),
        crud_case: UserCrudCase = Depends(get_crud_case)
    ):
        self.__limit = limit
        self.__offset = offset
        self.__order = order
        self.__crud_case = crud_case

    async def __read_many(self, limit: int, offset: int, order: Order) -> list[User]:
        return await self.__crud_case.read_all(limit, offset, order)

    async def __count(self) -> int:
        return await self.__crud_case.count()

    @staticmethod
    def __create_answer(users: list[User], count: int) -> UsersJsonResponse:
        users_out = [UserOut(**user.model_dump()) for user in users]

        return UsersJsonResponse(
            success=True,
            answer=UsersWrapper(
                entities=users_out,
                count=count
            )
        )

    async def answer(self) -> UsersJsonResponse:
        users = await self.__read_many(self.__limit, self.__offset, self.__order)
        count = await self.__count()
        return self.__create_answer(users, count)
