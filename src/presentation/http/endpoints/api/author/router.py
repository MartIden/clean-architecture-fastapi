from fastapi import APIRouter, Depends
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from src.domain.author.dto.response import AuthorJsonResponse, AuthorsJsonResponse
from src.kernel.fastapi.config import get_app_settings
from src.kernel.fastapi.settings.app import AppSettings
from src.presentation.http.endpoints.api.author.controllers.creator import AuthorCreatorController
from src.presentation.http.endpoints.api.author.controllers.deleter import AuthorDeleterController
from src.presentation.http.endpoints.api.author.controllers.many_reader import AuthorManyReaderController
from src.presentation.http.endpoints.api.author.controllers.reader import AuthorReaderController
from src.presentation.http.endpoints.api.author.controllers.updater import AuthorUpdaterController

author_api = APIRouter(prefix="/author", tags=["author"])


@author_api.post(
    "",
    status_code=HTTP_201_CREATED,
    response_model=AuthorJsonResponse,
    summary="Создать нового автора",
)
async def create_author(controller: AuthorCreatorController = Depends()):
    return await controller.run()


@author_api.get(
    "",
    status_code=HTTP_200_OK,
    response_model=AuthorJsonResponse,
    summary="Получить автора по идентификатору",
)
async def read_author(controller: AuthorReaderController = Depends()):
    return await controller.run()


@author_api.get(
    "/many",
    status_code=HTTP_200_OK,
    response_model=AuthorsJsonResponse,
    summary="Получить несколько авторов",
)
async def read_many_authors(controller: AuthorManyReaderController = Depends()):
    return await controller.run()


@author_api.put(
    "",
    status_code=HTTP_200_OK,
    response_model=AuthorJsonResponse,
    summary="Обновить автора",
)
async def update_author(controller: AuthorUpdaterController = Depends()):
    return await controller.run()


@author_api.delete(
    "",
    status_code=HTTP_201_CREATED,
    response_model=AuthorJsonResponse,
    summary="Обновить автора",
)
async def delete_author(controller: AuthorDeleterController = Depends()):
    return await controller.run()
