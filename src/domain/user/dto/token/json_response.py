from src.domain.common.dto import JsonResponse, JsonDto
from src.domain.common.value_obj.created_at import CreatedAt
from src.domain.common.value_obj.expired_at import ExpiredAt
from src.domain.common.value_obj.id import Id
from src.domain.common.value_obj.updated_at import UpdatedAt
from src.domain.user.value_obj.access import AccessToken


class TokenOut(JsonDto):
    id: Id

    access_token: AccessToken
    is_active: bool
    user_id: Id
    expired_at: ExpiredAt | None = None

    created_at: CreatedAt
    updated_at: UpdatedAt


class TokenJsonResponse(JsonResponse):
    answer: TokenOut | None = None


class TokensWrapper(JsonDto):
    entities: list[TokenOut]
    count: int


class TokensJsonResponse(JsonResponse):
    answer: TokensWrapper | None = None
