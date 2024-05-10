from abc import abstractmethod


from src.domain.book.dto.new_book import NewBook
from src.domain.book.dto.update_book import UpdateBook
from src.domain.book.entity.book import Book
from src.kernel.database.postgres.i_repository import IRepository


class IBookRepoPort(IRepository):

    @abstractmethod
    async def create(self, schema: NewBook) -> Book: ...

    @abstractmethod
    async def update(self, schema: UpdateBook) -> Book: ...

    @abstractmethod
    async def read_by_user(self, user_id: int) -> list[Book]: ...
