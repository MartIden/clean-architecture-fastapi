from fastapi import Depends

from src.application.author.cases.author_crud import AuthorCrudCase
from src.infrastructure.persistence.postgres.repositories.author_repo import AuthorRepo
from src.presentation.http.depends.postgres_repo import get_repository


def get_author_crud(repo: AuthorRepo = Depends(get_repository(repo_type=AuthorRepo))) -> AuthorCrudCase:
    return AuthorCrudCase(repo)
