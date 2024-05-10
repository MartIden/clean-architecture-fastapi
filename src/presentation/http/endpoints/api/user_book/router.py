from fastapi import APIRouter, Depends
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from src.domain.book.dto.response_user_book import UserBookJsonResponse, UserBooksJsonResponse
from src.presentation.http.endpoints.api.user_book.controller.creator import UserBookCreatorController
from src.presentation.http.endpoints.api.user_book.controller.delete import UserBookDeleterController
from src.presentation.http.endpoints.api.user_book.controller.reader import UserBookReaderController
from src.presentation.http.endpoints.api.user_book.controller.reader_by_user import UserBookReaderByUserController

user_book_api = APIRouter(prefix="/user-book", tags=["user-book"])


@user_book_api.post(
    "",
    status_code=HTTP_201_CREATED,
    response_model=UserBookJsonResponse,
    summary="Создать новую связь книга-пользователь",
)
async def create_user_book(controller: UserBookCreatorController = Depends()):
    return await controller.run()


@user_book_api.get(
    "",
    status_code=HTTP_200_OK,
    response_model=UserBookJsonResponse,
    summary="Возвращает связь книга-пользователь",
)
async def read_user_book(controller: UserBookReaderController = Depends()):
    return await controller.run()


@user_book_api.delete(
    "",
    status_code=HTTP_200_OK,
    response_model=UserBookJsonResponse,
    summary="Удаляет связь книга-пользователь",
)
async def delete_user_book(controller: UserBookDeleterController = Depends()):
    return await controller.run()


@user_book_api.get(
    "/{user_id}",
    status_code=HTTP_200_OK,
    response_model=UserBooksJsonResponse,
    summary="Возвращает связи книга-пользователь по конкретному пользователю",
)
async def get_user_book(controller: UserBookReaderByUserController = Depends()):
    return await controller.run()
