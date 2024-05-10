from abc import ABC, abstractmethod
from typing import Any

from src.kernel.fastapi.persistence.pools import DatabasePools
from src.kernel.rmq.connector import BaseRMQConnector
from src.kernel.rmq.handlers.abstract_handler import AbstractRmqHandler


class AbstractRmqHandlerCreator(ABC):
    def __init__(
        self,
        message: Any,
        rmq_connector: BaseRMQConnector,
        db_connection_pools: DatabasePools,
    ):
        self._message = message
        self._rmq_connector = rmq_connector
        self._db_connection_pools = db_connection_pools

    @abstractmethod
    def create(self) -> AbstractRmqHandler:
        pass
