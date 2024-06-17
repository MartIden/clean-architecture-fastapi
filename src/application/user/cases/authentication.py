from src.application.user.cases.password import UserPasswordService
from src.domain.user.entity.user import User
from src.domain.user.user.user_repo import IUserRepoPort


class UserAuthenticationCase:

    def __init__(self, user_repo: IUserRepoPort, salt: str):
        self.__salt = salt
        self.__user_repo = user_repo

    @staticmethod
    def __hash_password(password: str, salt: str) -> str:
        return UserPasswordService.create_password(password, salt)

    async def is_authenticated(self, login: str, password: str) -> User | None:
        hashed_password = self.__hash_password(password, self.__salt)
        user = await self.__user_repo.read_by_login(login, hashed_password)
        return user
