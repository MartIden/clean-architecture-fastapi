from src.kernel.fastapi.config import get_app_settings
from src.presentation.amqp.consumers.new_book import NewBookConsumer

consumers = {
    "prod": [],
    "dev": [NewBookConsumer],
    "test": [],
}


def get_consumers() -> list:
    app_settings = get_app_settings()
    env = app_settings.app_env.value.lower()
    return consumers.get(env)


rmq_consumers = get_consumers()

__all__ = ["rmq_consumers"]
