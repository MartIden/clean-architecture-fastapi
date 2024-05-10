from src.domain.user.entity.user import User
from src.domain.user.ports.user_repo import IUserRepoPort


class UserByTokenGetterCase:

    def __init__(self, user_repo: IUserRepoPort):
        self.__user_repo = user_repo

    async def get_user(self, token: str) -> User | None:
        return await self.__user_repo.read_by_token(token)
