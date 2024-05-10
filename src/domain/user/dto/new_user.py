from src.domain.common.dto import JsonRequest
from src.domain.user.value_obj.email import Email
from src.domain.user.value_obj.login import Login
from src.domain.user.value_obj.password import Password


class NewUser(JsonRequest):
    login: Login
    password: Password
    email: Email
