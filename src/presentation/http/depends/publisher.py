from typing import Callable, Type

from fastapi import Depends

from src.kernel.fastapi.config import get_app_settings
from src.kernel.fastapi.settings.app import AppSettings
from src.kernel.rmq.connector import BaseRMQConnector
from src.kernel.rmq.dependencies import get_rmq_connector
from src.kernel.rmq.publisher import AbstractRMQPublisher


def get_publisher(
    publisher_type: Type[AbstractRMQPublisher],
) -> Callable[[BaseRMQConnector], AbstractRMQPublisher]:
    def _get_pub(
        rmq_connector: BaseRMQConnector = Depends(get_rmq_connector),
        app_settings: AppSettings = Depends(get_app_settings),
    ) -> AbstractRMQPublisher:
        return publisher_type(rmq_connector, app_settings)

    return _get_pub
