from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class IRedisRepoPort(ABC):

    @abstractmethod
    async def add_model(self, key: str, model: BaseModel) -> int:
        pass

    @abstractmethod
    async def ping(self):
        pass

    @abstractmethod
    async def get(self, key: str) -> Any:
        pass

    @abstractmethod
    async def get_list(self, key: str, start=0, end=1) -> Any:
        pass

    @abstractmethod
    async def delete(self, key: str):
        pass
