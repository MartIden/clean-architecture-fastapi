from src.domain.common.entity import Entity
from src.domain.common.value_obj.expired_at import ExpiredAt
from src.domain.common.value_obj.id import Id
from src.domain.user.value_obj.access import AccessToken


class Token(Entity):
    user_id: Id
    access_token: AccessToken
    is_active: bool
    expired_at: ExpiredAt | None = None
