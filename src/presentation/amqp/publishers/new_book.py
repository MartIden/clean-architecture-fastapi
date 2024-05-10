from typing import Optional

from src.kernel.rmq.publisher import BaseRMQPublisher


class NewBookPublisher(BaseRMQPublisher):
    @property
    def _exchange_name(self) -> Optional[str]:
        exchanges = self._app_settings.RMQ_RUN_SETTINGS.exchanges
        return exchanges.get("new_book").name
