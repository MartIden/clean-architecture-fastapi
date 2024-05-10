from src.domain.common.entity import Entity
from src.domain.user.value_obj.email import Email
from src.domain.user.value_obj.login import Login
from src.domain.user.value_obj.password import Password


class User(Entity):
    login: Login
    password: Password
    email: Email
