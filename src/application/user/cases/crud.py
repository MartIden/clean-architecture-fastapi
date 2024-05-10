from pydantic import BaseModel
from pypika import Order

from src.domain.user.dto.new_user import NewUser
from src.domain.user.dto.update_user import UpdateUser
from src.domain.user.entity.user import User
from src.domain.user.exceptions.user import UserIsNotExists
from src.ports.user.user_repo import IUserRepoPort


class UserCrudCase:

    def __init__(self, repo: IUserRepoPort):
        self.__repo = repo

    @staticmethod
    def __raise_if_not_exist(user: User | BaseModel) -> None:
        if not user:
            raise UserIsNotExists("User With Current Id Is Not Exist")
    
    async def create(self, schema: NewUser) -> User:
        user = await self.__repo.create(schema)
        self.__raise_if_not_exist(user)
        return user

    async def read(self, row_id: int) -> User | None:
        user = await self.__repo.read(row_id)
        self.__raise_if_not_exist(user)
        return user

    async def update(self, schema: UpdateUser) -> User:
        user = await self.__repo.update(schema)
        self.__raise_if_not_exist(user)
        return user

    async def delete(self, row_id: int) -> User | BaseModel | None:
        user = await self.__repo.delete(row_id)
        self.__raise_if_not_exist(user)
        return user

    async def read_all(self, limit: int, offset: int, order: Order) -> list[User | BaseModel]:
        return await self.__repo.read_all(limit, offset, order)

    async def count(self) -> int:
        return await self.__repo.count()
