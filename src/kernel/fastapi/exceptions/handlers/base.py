import traceback

from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND
)
from starlette_context import context

from src.kernel.fastapi.config import get_app_settings
from src.kernel.logging.json_logger_getter import get_json_logger

APP_SETTINGS = get_app_settings()


def __base_error_handler(
    status: int,
    exc: HTTPException,
    logger=get_json_logger(),
    app_settings=get_app_settings()
) -> JSONResponse:

    error = {
        "error_type": type(exc).__name__,
        "error_message": str(exc),
    }

    if app_settings.SHOW_TRACEBACK_IN_RESPONSE:
        error["traceback"] = traceback.format_tb(exc.__traceback__)

    extra = {
        "success": False,
        "answer": None,
        "error": error,
    }

    json_response = JSONResponse(status_code=status, content=extra)

    extra["error"]["traceback"] = traceback.format_tb(exc.__traceback__)
    extra.update(context.data)

    logger.error(msg=type(exc).__name__, extra=extra)

    return json_response


async def http_error_handler(
    _: Request,
    exc: HTTPException,
    logger=get_json_logger(),
) -> JSONResponse:
    return __base_error_handler(HTTP_500_INTERNAL_SERVER_ERROR, exc=exc, logger=logger)


async def http_business_error_handler(
    _: Request,
    exc: HTTPException,
    logger=get_json_logger(),
) -> JSONResponse:
    return __base_error_handler(HTTP_200_OK, exc=exc, logger=logger)


async def http_validation_error_handler(
    _: Request,
    exc: HTTPException,
    logger=get_json_logger(),
) -> JSONResponse:
    return __base_error_handler(HTTP_422_UNPROCESSABLE_ENTITY, exc=exc, logger=logger)


async def http_auth_error_handler(
    _: Request,
    exc: HTTPException,
    logger=get_json_logger(),
) -> JSONResponse:
    return __base_error_handler(HTTP_401_UNAUTHORIZED, exc=exc, logger=logger)


async def not_found_error_handler(
    _: Request,
    exc: HTTPException,
    logger=get_json_logger(),
) -> JSONResponse:
    return __base_error_handler(HTTP_404_NOT_FOUND, exc=exc, logger=logger)
