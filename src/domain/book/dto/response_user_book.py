from src.domain.common.dto import JsonDto, JsonResponse
from src.domain.common.value_obj.created_at import CreatedAt
from src.domain.common.value_obj.id import Id
from src.domain.common.value_obj.updated_at import UpdatedAt


class UserBookOut(JsonDto):
    id: Id

    user_id: Id
    book_id: Id

    created_at: CreatedAt
    updated_at: UpdatedAt


class UserBookJsonResponse(JsonResponse):
    answer: UserBookOut | None = None


class UsersBooksWrapper(JsonDto):
    entities: list[UserBookOut] | None = None
    count: int


class UserBooksJsonResponse(JsonResponse):
    answer: UsersBooksWrapper | None = None
