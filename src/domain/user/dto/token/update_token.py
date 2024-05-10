from pydantic import BaseModel

from src.domain.common.value_obj.created_at import CreatedAt
from src.domain.common.value_obj.id import Id
from src.domain.common.value_obj.updated_at import UpdatedAt
from src.domain.user.value_obj.access import AccessToken


class UpdateToken(BaseModel):

    id: Id

    user_id: Id | None = None
    access_token: AccessToken | None = None
    is_active: bool | None = None

    created_at: CreatedAt | None = None
    updated_at: UpdatedAt | None = None
