from pydantic import BaseModel

from src.domain.common.value_obj.id import Id
from src.domain.user.value_obj.access import AccessToken
from src.domain.common.dto import JsonRequest
from src.domain.user.value_obj.login import Login
from src.domain.user.value_obj.password import Password


class NewTokenRequest(JsonRequest):
    login: Login
    password: Password


class NewToken(BaseModel):
    user_id: Id
    access_token: AccessToken
    is_active: bool
