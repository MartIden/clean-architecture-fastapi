from abc import ABC, abstractmethod
from logging import INFO, Logger
from typing import Optional, Any

from src.kernel.logging.json_logger_getter import get_json_logger


class AbstractRmqHandler(ABC):

    _logger = None

    @property
    def __logger(self) -> Logger:
        if not self._logger:
            self._logger = get_json_logger()
        return self._logger

    def __set_extra(self, input_message: Optional[Any], extra: Optional[dict] = None) -> dict:
        prepared_extra = {"handler": self.handler_name, "input_message": input_message}

        if extra:
            prepared_extra = {**prepared_extra, **extra}
        return prepared_extra

    def _log_handler(
        self,
        *,
        extra: Optional[dict] = None,
        message: Optional[str] = None,
        input_message: Optional[Any] = None,
        level=INFO
    ) -> None:
        extra = self.__set_extra(input_message, extra)
        self.__logger.log(level, msg=message, extra=extra)

    @property
    def handler_name(self) -> str:
        return type(self).__name__

    @abstractmethod
    async def handle(self) -> None:
        pass
