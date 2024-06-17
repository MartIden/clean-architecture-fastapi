from src.domain.user.entity.user import User
from src.domain.user.exceptions.user import UserIsNotExistsError


class UserValidatorCase:

    def __init__(self, user: User) -> None:
        self.__user = user

    def validate(self) -> None:

        if not self.__user:
            raise UserIsNotExistsError("User Is Not Exists")
