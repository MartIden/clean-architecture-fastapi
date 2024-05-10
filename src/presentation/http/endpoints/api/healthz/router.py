from typing import Union

from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK

from src.domain import HealthAnswerDTO
from src.domain import JsonHttpResponse
from src.external.presentation.input.http.endpoints.api.healthz.controller import HealthCheckController


health_api = APIRouter(prefix="/healthz", tags=["health"])


@health_api.get(
    "",
    status_code=HTTP_200_OK,
    response_model=HealthAnswerDTO,
    summary="Проверка доступности приложения",
)
async def health_get(
    health_check_controller: HealthCheckController = Depends(HealthCheckController),
) -> Union[HealthAnswerDTO, JsonHttpResponse]:
    return await health_check_controller.run()
