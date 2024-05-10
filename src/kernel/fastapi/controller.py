from abc import ABC, abstractmethod
from typing import Optional, Union
from logging import Logger
import logging


from starlette.responses import Response
from pydantic import BaseModel
from starlette_context import context

from src.domain.common.dto import JsonResponse
from src.kernel.logging.json_logger_getter import get_json_logger


class ControllerLogger:

    __logger: Optional[Logger] = None

    def __init__(self, controller_obj: "IJsonController"):
        self.__controller_obj = controller_obj

    @property
    def context(self) -> dict:
        return context.data

    @property
    def logger(self) -> Logger:
        if not self.__logger:
            self.__logger = get_json_logger()
        return self.__logger

    @property
    def controller_name(self) -> str:
        return str(type(self.__controller_obj).__name__)

    @property
    def message(self) -> str:
        return f"Answer of '{self.controller_name}' controller"

    def create_extra(self, extra: dict) -> dict:
        extra = extra if extra else {}
        message = extra.get("message")

        if message:
            extra["message_"] = extra.get("message")
            del extra["message"]

        extra["controller"] = self.controller_name
        extra = {**extra, **self.context}

        return extra

    def log_answer(self, extra: BaseModel, log_level=logging.INFO) -> None:
        extra = self.create_extra(extra.dict())
        self.log_controller(self.message, extra=extra, log_level=log_level)

    def log_controller(
        self, message: Optional[str] = None, extra: Optional[dict] = None, log_level=logging.INFO
    ) -> None:
        extra = self.create_extra(extra)
        self.logger.log(log_level, message, extra=extra)


class IJsonController(ABC):

    __controller_logger: Optional[ControllerLogger] = None

    @property
    def _controller_logger(self) -> ControllerLogger:
        if not self.__controller_logger:
            self.__controller_logger = ControllerLogger(self)
        return self.__controller_logger

    def log_answer(self, answer: BaseModel, log_level=20) -> None:
        self._controller_logger.log_answer(answer, log_level)

    def _log_controller(self, message: str, extra: dict, log_level=logging.INFO) -> None:
        self._controller_logger.log_controller(message, extra, log_level)

    @abstractmethod
    async def answer(self) -> JsonResponse:
        pass

    async def run(self) -> Union[BaseModel, JsonResponse]:
        answer = await self.answer()
        self.log_answer(answer)
        return answer


class IViewController(ABC):
    @abstractmethod
    async def answer(self) -> Response:
        pass
