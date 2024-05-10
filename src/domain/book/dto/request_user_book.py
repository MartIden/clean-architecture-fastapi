from src.domain.common.dto import JsonRequest
from src.domain.common.value_obj.created_at import CreatedAt
from src.domain.common.value_obj.id import Id
from src.domain.common.value_obj.updated_at import UpdatedAt


class NewUserBookRequest(JsonRequest):
    book_id: Id


class UpdateUserBookRequest(JsonRequest):
    id: Id

    user_id: Id | None = None
    book_id: Id | None = None

    created_at: CreatedAt | None = None
    updated_at: UpdatedAt | None = None
