from fastapi import APIRouter

from src.presentation.http.endpoints.api.author.router import author_api
from src.presentation.http.endpoints.api.book.router import book_api
from src.presentation.http.endpoints.api.user.router import user_api
from src.presentation.http.endpoints.api.user_book.router import user_book_api

""" API ROUTER """
client_router = APIRouter(prefix="/api/v1")

client_router.include_router(book_api)
client_router.include_router(user_api)
client_router.include_router(author_api)
client_router.include_router(user_book_api)
