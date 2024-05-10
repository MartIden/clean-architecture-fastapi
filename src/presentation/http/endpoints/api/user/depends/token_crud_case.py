from fastapi import Depends

from src.application.user.cases.token_crud import TokenCrudCase
from src.infrastructure.persistence.postgres.repositories.token_repo import TokenRepo
from src.presentation.http.depends.postgres_repo import get_repository


def get_token_crud_service(repo: TokenRepo = Depends(get_repository(repo_type=TokenRepo))) -> TokenCrudCase:
    return TokenCrudCase(repo)
