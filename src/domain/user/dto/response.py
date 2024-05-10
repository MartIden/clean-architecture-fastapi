from src.domain.common.dto import JsonResponse
from src.domain.common.dto import JsonDto
from src.domain.common.value_obj.created_at import CreatedAt
from src.domain.common.value_obj.id import Id
from src.domain.common.value_obj.updated_at import UpdatedAt
from src.domain.user.value_obj.email import Email
from src.domain.user.value_obj.login import Login


class UserOut(JsonDto):

    id: Id

    login: Login
    email: Email

    created_at: CreatedAt
    updated_at: UpdatedAt


class UsersWrapper(JsonDto):
    entities: list[UserOut] = None
    count: int


class UserJsonResponse(JsonResponse):
    answer: UserOut | None = None


class UsersJsonResponse(JsonResponse):
    answer: UsersWrapper | None = None
