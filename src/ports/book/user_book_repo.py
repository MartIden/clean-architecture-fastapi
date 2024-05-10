from abc import abstractmethod


from src.domain.book.dto.new_user_book import NewUserBook
from src.domain.book.dto.update_user_book import UpdateUserBook
from src.domain.book.entity.user_book import UserBook
from src.kernel.database.postgres.i_repository import IRepository


class IUserBookRepoPort(IRepository):

    @abstractmethod
    async def create(self, schema: NewUserBook) -> UserBook: ...

    @abstractmethod
    async def update(self, schema: UpdateUserBook) -> UserBook: ...

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> list[UserBook]: ...

    @abstractmethod
    async def count_by_user_id(self, user_id: int) -> int: ...
