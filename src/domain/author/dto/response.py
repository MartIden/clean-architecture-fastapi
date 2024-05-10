from src.domain.author.value_obj.name import Name
from src.domain.author.value_obj.surname import Surname
from src.domain.common.dto import JsonDto, JsonResponse
from src.domain.common.value_obj.created_at import CreatedAt
from src.domain.common.value_obj.id import Id
from src.domain.common.value_obj.updated_at import UpdatedAt


class AuthorOut(JsonDto):
    id: Id

    name: Name
    surname: Surname

    created_at: CreatedAt
    updated_at: UpdatedAt


class AuthorJsonResponse(JsonResponse):
    answer: AuthorOut | None = None


class AuthorsWrapper(JsonDto):
    entities: list[AuthorOut] | None = None
    count: int


class AuthorsJsonResponse(JsonResponse):
    answer: AuthorsWrapper | None = None
