import datetime

from src.domain.user.entity.token import Token
from src.domain.user.exceptions.token import IncorrectAuthToken


class TokenValidatorCase:

    def __init__(self, token: Token) -> None:
        self.__token = token

    def validate(self) -> None:

        if not self.__token:
            raise IncorrectAuthToken("Token Is Not Exist")

        if not self.__token.is_active:
            raise IncorrectAuthToken("Token Is Not Active")

        if self.__token.expired_at < int(datetime.datetime.now().timestamp()):
            raise IncorrectAuthToken("Token Is Expired")
