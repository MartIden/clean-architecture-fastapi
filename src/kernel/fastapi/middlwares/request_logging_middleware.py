import json
from logging import Logger

from fastapi import Request
from starlette_context import context

from src.kernel.fastapi.config import get_app_settings
from src.kernel.logging.json_logger_getter import get_json_logger


class RequestJSONLoggerMiddleware:
    def __init__(self, request: Request, logger: Logger):
        self.__logger = logger
        self.__request: Request = request

    @property
    async def log_message(self) -> dict:
        unprepared_body = str(await self.__request.body(), "utf-8")

        try:
            body = json.loads(unprepared_body)
        except json.decoder.JSONDecodeError:
            body = unprepared_body

        return {
            "url": self.__request.url.path,
            "method": self.__request.method,
            "queries": self.__request.query_params,
            "body": body,
            **context.data,
        }

    async def log(self):
        log = await self.log_message
        self.__logger.info("request_data", extra=log)

    @staticmethod
    async def log_middle(request: Request):
        try:
            logger = get_json_logger()
            logging_middleware = RequestJSONLoggerMiddleware(request, logger)
            await logging_middleware.log()
        except Exception:
            pass
