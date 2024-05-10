from fastapi import Depends

from src.application.user.cases.crud import UserCrudCase
from src.infrastructure.persistence.postgres.repositories.user_repo import UserRepo
from src.presentation.http.depends.postgres_repo import get_repository


def get_crud_case(repo: UserRepo = Depends(get_repository(repo_type=UserRepo))) -> UserCrudCase:
    return UserCrudCase(repo)
