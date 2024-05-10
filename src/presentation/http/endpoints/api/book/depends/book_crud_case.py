from fastapi import Depends

from src.application.book.cases.book_crud import BookCrudCase
from src.infrastructure.persistence.postgres.repositories.book_repo import BookRepo
from src.presentation.http.depends.postgres_repo import get_repository


def get_book_crud_case(repo: BookRepo = Depends(get_repository(repo_type=BookRepo))) -> BookCrudCase:
    return BookCrudCase(repo)
