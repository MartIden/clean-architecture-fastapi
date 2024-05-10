from src.kernel.rmq.consumer import BaseHandlersRunnerRMQConsumer
from src.presentation.amqp.handlers.new_book.factory import NewBookHandlerFactory


class NewBookConsumer(BaseHandlersRunnerRMQConsumer):

    _handlers_factories = [
        NewBookHandlerFactory,
    ]

    @property
    def _auto_ack(self) -> bool:
        return True

    @property
    def _exchange_name(self) -> str:
        exchanges = self._app_settings.RMQ_RUN_SETTINGS.exchanges
        return exchanges.get("new_book").name

    @property
    def _queue_name(self) -> str:
        queue = self._app_settings.RMQ_RUN_SETTINGS.queues
        return queue.get("new_book").name
