from fastapi import Depends

from src.application.book.cases.user_book_crud import UserBookCrudCase
from src.infrastructure.persistence.postgres.repositories.user_book_repo import UserBookRepo
from src.presentation.http.depends.postgres_repo import get_repository


def get_user_book_crud_case(repo: UserBookRepo = Depends(get_repository(repo_type=UserBookRepo))) -> UserBookCrudCase:
    return UserBookCrudCase(repo)
