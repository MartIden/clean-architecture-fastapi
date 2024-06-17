from abc import ABC, abstractmethod
from typing import Any

from fastapi import FastAPI

from src.kernel.rmq.connector import BaseRMQConnector
from src.kernel.rmq.handlers.abstract_handler import AbstractRmqHandler


class AbstractRmqHandlerCreator(ABC):
    def __init__(
        self,
        message: Any,
        rmq_connector: BaseRMQConnector,
        application: FastAPI,
    ):
        self._message = message
        self._rmq_connector = rmq_connector
        self._application = application

    @abstractmethod
    def create(self) -> AbstractRmqHandler:
        pass
