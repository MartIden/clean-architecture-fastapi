from abc import abstractmethod


from src.domain.user.dto.token.new_token import NewToken
from src.domain.user.dto.token.update_token import UpdateToken
from src.domain.user.entity.token import Token
from src.kernel.database.postgres.i_repository import IRepository


class ITokenRepoPort(IRepository):

    @abstractmethod
    async def create(self, schema: NewToken) -> Token: ...

    @abstractmethod
    async def update(self, schema: UpdateToken) -> Token: ...

    @abstractmethod
    async def read_by_token(self, token: str) -> Token: ...
