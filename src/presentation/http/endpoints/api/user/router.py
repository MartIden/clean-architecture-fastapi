from fastapi import APIRouter, Depends
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from src.domain.book.dto.response_user_book import UserBooksJsonResponse
from src.domain.user.dto.token.json_response import TokenJsonResponse
from src.domain.user.dto.response import UserJsonResponse, UsersJsonResponse
from src.presentation.http.endpoints.api.user.controllers.creator import UserCreatorController
from src.presentation.http.endpoints.api.user.controllers.deleter import UserDeleterController
from src.presentation.http.endpoints.api.user.controllers.many_reader import UserManyReaderController
from src.presentation.http.endpoints.api.user.controllers.reader import UserReaderController
from src.presentation.http.endpoints.api.user.controllers.token.creator import TokenCreatorController
from src.presentation.http.endpoints.api.user.controllers.updater import UserUpdaterController
from src.presentation.http.endpoints.api.user_book.controller.reader_by_user import UserBookReaderByUserController

user_api = APIRouter(prefix="/user", tags=["user"])


@user_api.post(
    "",
    status_code=HTTP_201_CREATED,
    response_model=UserJsonResponse,
    summary="Создать нового пользователя",
)
async def create_user(controller: UserCreatorController = Depends()):
    return await controller.run()


@user_api.get(
    "",
    status_code=HTTP_200_OK,
    response_model=UserJsonResponse,
    summary="Вернуть пользователя по идентификатору",
)
async def read_user(controller: UserReaderController = Depends()):
    return await controller.run()


@user_api.get(
    "/many",
    status_code=HTTP_200_OK,
    response_model=UsersJsonResponse,
    summary="Вернуть несколько пользователей",
)
async def read_many_users(controller: UserManyReaderController = Depends()):
    return await controller.run()


@user_api.put(
    "",
    status_code=HTTP_200_OK,
    response_model=UserJsonResponse,
    summary="Обновить пользователя",
)
async def update_user(controller: UserUpdaterController = Depends()):
    return await controller.run()


@user_api.delete(
    "",
    status_code=HTTP_201_CREATED,
    response_model=UserJsonResponse,
    summary="Удалить пользователя",
)
async def delete_user(controller: UserDeleterController = Depends()):
    return await controller.run()


@user_api.post(
    "/token",
    status_code=HTTP_201_CREATED,
    response_model=TokenJsonResponse,
    summary="Создать новый токен пользователя",
)
async def create_token(controller: TokenCreatorController = Depends()):
    return await controller.run()


@user_api.get(
    "/{user_id}/books",
    status_code=HTTP_200_OK,
    response_model=UserBooksJsonResponse,
    summary="Возвращает книги по конкретному пользователю",
)
async def get_user_book(controller: UserBookReaderByUserController = Depends()):
    return await controller.run()
