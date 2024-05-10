from pydantic import BaseModel

from src.domain.common.value_obj.id import Id
from src.domain.user.value_obj.email import Email
from src.domain.user.value_obj.login import Login
from src.domain.user.value_obj.password import Password


class UpdateUser(BaseModel):

    id: Id

    login: Login | None = None
    password: Password | None = None
    email: Email | None = None
