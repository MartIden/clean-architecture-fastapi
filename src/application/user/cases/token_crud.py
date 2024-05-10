from pydantic import BaseModel
from pypika import Order

from src.domain.user.dto.token.new_token import NewToken
from src.domain.user.dto.token.update_token import UpdateToken
from src.domain.user.entity.token import Token
from src.domain.user.exceptions.token import TokenIsNotExists
from src.domain.user.ports.token_repo import ITokenRepoPort


class TokenCrudCase:

    def __init__(self, repo: ITokenRepoPort):
        self.__repo = repo

    @staticmethod
    def __raise_if_not_exist(token: Token | BaseModel) -> None:
        if not token:
            raise TokenIsNotExists("Token With Current Id Is Not Exist")
    
    async def create(self, schema: NewToken) -> Token:
        token = await self.__repo.create(schema)
        self.__raise_if_not_exist(token)
        return token

    async def read(self, row_id: int) -> Token | None:
        token = await self.__repo.read(row_id)
        self.__raise_if_not_exist(token)
        return token

    async def update(self, schema: UpdateToken) -> Token:
        token = await self.__repo.update(schema)
        self.__raise_if_not_exist(token)
        return token

    async def delete(self, row_id: int) -> Token | BaseModel | None:
        token = await self.__repo.delete(row_id)
        self.__raise_if_not_exist(token)
        return token

    async def read_all(self, limit: int, offset: int, order: Order) -> list[Token | BaseModel]:
        return await self.__repo.read_all(limit, offset, order)

    async def read_by_token(self, token: str) -> Token | None:
        return await self.__repo.read_by_token(token)

    async def count(self) -> int:
        return await self.__repo.count()
