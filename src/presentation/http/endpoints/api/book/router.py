from fastapi import APIRouter, Depends
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from src.domain.book.dto.response import BookJsonResponse, BooksJsonResponse
from src.presentation.http.endpoints.api.book.controllers.creator import BookCreatorController
from src.presentation.http.endpoints.api.book.controllers.deleter import BookDeleterController
from src.presentation.http.endpoints.api.book.controllers.many_reader import BookReaderManyController
from src.presentation.http.endpoints.api.book.controllers.reader import BookReaderController
from src.presentation.http.endpoints.api.book.controllers.updater import BookUpdaterController


book_api = APIRouter(prefix="/book", tags=["book"])


@book_api.post(
    "",
    status_code=HTTP_201_CREATED,
    response_model=BookJsonResponse,
    summary="Создать новую книгу",
)
async def create_book(controller: BookCreatorController = Depends()):
    return await controller.run()


@book_api.get(
    "",
    status_code=HTTP_200_OK,
    response_model=BookJsonResponse,
    summary="Вернуть книгу по идентификатору",
)
async def read_book(controller: BookReaderController = Depends()):
    return await controller.run()


@book_api.get(
    "/many",
    status_code=HTTP_200_OK,
    response_model=BooksJsonResponse,
    summary="Вернуть несколько книг",
)
async def read_book(controller: BookReaderManyController = Depends()):
    return await controller.run()


@book_api.put(
    "",
    status_code=HTTP_200_OK,
    response_model=BookJsonResponse,
    summary="Обновить книгу",
)
async def update_book(controller: BookUpdaterController = Depends()):
    return await controller.run()


@book_api.delete(
    "",
    status_code=HTTP_200_OK,
    response_model=BookJsonResponse,
    summary="Удалить книгу",
)
async def delete_book(controller: BookDeleterController = Depends()):
    return await controller.run()
