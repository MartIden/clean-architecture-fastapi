import datetime

from src.domain.user.entity.token import Token
from src.domain.user.exceptions.token import IncorrectAuthTokenError


class TokenValidatorCase:

    def __init__(self, token: Token) -> None:
        self.__token = token

    def validate(self) -> None:

        if not self.__token:
            raise IncorrectAuthTokenError("Token Is Not Exist")

        if not self.__token.is_active:
            raise IncorrectAuthTokenError("Token Is Not Active")

        if self.__token.expired_at < int(datetime.datetime.now().timestamp()):
            raise IncorrectAuthTokenError("Token Is Expired")
