from src.domain.author.value_obj.name import Name
from src.domain.author.value_obj.surname import Surname
from src.domain.common.dto import JsonRequest
from src.domain.common.value_obj.id import Id


class NewAuthorRequest(JsonRequest):
    name: Name
    surname: Surname


class UpdateAuthorRequest(JsonRequest):
    id: Id

    name: Name | None = None
    surname: Surname | None = None
