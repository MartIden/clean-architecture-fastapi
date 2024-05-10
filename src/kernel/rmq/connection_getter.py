import asyncio

from src.kernel.fastapi.settings.app import AppSettings
from src.kernel.rmq.connector import BaseRMQConnector
from src.kernel.rmq.events.runner import get_amqp_uri


def get_connector(app_settings: AppSettings):
    loop = asyncio.get_running_loop()
    return BaseRMQConnector(amqp_uri=get_amqp_uri(app_settings), loop=loop)
