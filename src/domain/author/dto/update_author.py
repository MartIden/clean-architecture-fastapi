from pydantic import BaseModel

from src.domain.author.value_obj.name import Name
from src.domain.author.value_obj.surname import Surname
from src.domain.common.value_obj.id import Id


class UpdateAuthor(BaseModel):
    id: Id

    name: Name | None = None
    surname: Surname | None = None
