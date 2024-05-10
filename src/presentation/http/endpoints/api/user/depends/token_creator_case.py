from fastapi import Depends

from src.application.user.cases.authentication import UserAuthenticationCase
from src.application.user.cases.token_creator import TokenCreatorCase
from src.application.user.cases.token_crud import TokenCrudCase
from src.infrastructure.persistence.postgres.repositories.token_repo import TokenRepo
from src.infrastructure.persistence.postgres.repositories.user_repo import UserRepo
from src.kernel.fastapi.config import get_app_settings
from src.kernel.fastapi.settings.app import AppSettings
from src.presentation.http.depends.postgres_repo import get_repository


def get_user_authentication_case(
    repo: UserRepo = Depends(get_repository(repo_type=UserRepo)),
    app_settings: AppSettings = Depends(get_app_settings)
) -> UserAuthenticationCase:
    return UserAuthenticationCase(repo, app_settings.SALT)


def get_token_crud_case(repo: TokenRepo = Depends(get_repository(repo_type=TokenRepo))) -> TokenCrudCase:
    return TokenCrudCase(repo)


def get_token_creator_case(
    user_authentication_case: UserAuthenticationCase = Depends(get_user_authentication_case),
    token_crud_case: TokenCrudCase = Depends(get_token_crud_case),
) -> TokenCreatorCase:
    return TokenCreatorCase(auth=user_authentication_case, token_crud=token_crud_case)
