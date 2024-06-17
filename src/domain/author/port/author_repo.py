from abc import abstractmethod


from src.domain.author.dto.new_author import NewAuthor
from src.domain.author.dto.update_author import UpdateAuthor
from src.domain.author.entity.author import Author
from src.kernel.database.postgres.i_repository import IRepository


class IAuthorRepoPort(IRepository):

    @abstractmethod
    async def create(self, schema: NewAuthor) -> Author: ...

    @abstractmethod
    async def update(self, schema: UpdateAuthor) -> Author: ...
