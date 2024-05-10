from starlette.requests import Request

from src.kernel.rmq.connector import BaseRMQConnector


def get_rmq_connector(request: Request) -> BaseRMQConnector:
    return request.app.rmq_connector
