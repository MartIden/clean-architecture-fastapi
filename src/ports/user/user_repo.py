from abc import abstractmethod


from src.domain.user.dto.new_user import NewUser
from src.domain.user.dto.update_user import UpdateUser
from src.domain.user.entity.user import User
from src.kernel.database.postgres.i_repository import IRepository


class IUserRepoPort(IRepository):

    @abstractmethod
    async def create(self, schema: NewUser) -> User: ...

    @abstractmethod
    async def update(self, schema: UpdateUser) -> User: ...

    @abstractmethod
    async def read_by_login(self, login: str, password: str) -> User: ...

    @abstractmethod
    async def read_by_token(self, token: str) -> User | None: ...
