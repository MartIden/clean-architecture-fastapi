import uuid

from src.application.user.cases.authentication import UserAuthenticationCase
from src.application.user.cases.token_crud import TokenCrudCase
from src.domain.user.dto.token.new_token import NewToken
from src.domain.user.entity.token import Token
from src.domain.user.exceptions.user import UserIsNotExistsError


class TokenCreatorCase:

    def __init__(self, auth: UserAuthenticationCase, token_crud: TokenCrudCase):
        self.__auth = auth
        self.__token_crud = token_crud

    @staticmethod
    def __generate_token() -> str:
        return str(uuid.uuid4())

    async def __create_token(self, id_: int, token: str) -> Token:
        return await self.__token_crud.create(
            NewToken(
                user_id=id_,
                access_token=token,
                is_active=True
            )
        )

    async def create_token(self, login: str, password: str) -> Token:
        user = await self.__auth.is_authenticated(login, password)

        if not user:
            raise UserIsNotExistsError("User With Current Login/Password Is Not Exist")

        uuid_str = self.__generate_token()
        return await self.__create_token(user.id, uuid_str)
