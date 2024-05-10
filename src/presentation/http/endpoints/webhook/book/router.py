from fastapi import APIRouter, Depends
from starlette.status import HTTP_201_CREATED

from src.domain.common.dto import JsonResponse
from src.presentation.http.endpoints.webhook.book.controllers.many_creator import BookManyTaskCreatorController

book_task_webhook = APIRouter(prefix="/book/task", tags=["webhook-book"])


@book_task_webhook.post(
    "/many",
    status_code=HTTP_201_CREATED,
    response_model=JsonResponse,
    summary="Отправить несколько задач на создание книг в exchange book.new",
)
async def create_book_task(controller: BookManyTaskCreatorController = Depends()):
    return await controller.run()
