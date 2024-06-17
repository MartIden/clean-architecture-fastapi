from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyHeader

from src.application.user.cases.token_crud import TokenCrudCase
from src.application.user.cases.token_validator import TokenValidatorCase
from src.application.user.cases.user_by_token_getter import UserByTokenGetterCase
from src.application.user.cases.user_validator import UserValidatorCase
from src.domain.user.entity.user import User
from src.domain.user.exceptions.token import IncorrectAuthTokenError
from src.infrastructure.persistence.postgres.repositories.user_repo import UserRepo
from src.presentation.http.depends.postgres_repo import get_repository
from src.presentation.http.endpoints.api.user.depends.token_crud_case import get_token_crud_service


def get_user_by_token_getter(repo: UserRepo = Depends(get_repository(repo_type=UserRepo))) -> UserByTokenGetterCase:
    return UserByTokenGetterCase(repo)


async def get_user_by_token(
    token: Annotated[str, Depends(APIKeyHeader(name='Authorization'))],
    user_by_token: UserByTokenGetterCase = Depends(get_user_by_token_getter),
    token_crud: TokenCrudCase = Depends(get_token_crud_service)
) -> User:

    token_model = await token_crud.read_by_token(token)
    TokenValidatorCase(token_model).validate()

    user = await user_by_token.get_user(token)
    UserValidatorCase(user).validate()

    return user
