from fastapi import FastAPI

from src.kernel.fastapi.persistence.pools import register_init_pools_handler
from src.kernel.fastapi.persistence.postgres.events import register_postgres_handler
from src.kernel.fastapi.settings.app import AppSettings
from src.kernel.logging.json_logger_getter import get_json_logger
from src.kernel.rmq.events.binder import register_rmq_bind_handler
from src.kernel.rmq.events.exchange_declarer import register_rmq_exchange_declare_handler
from src.kernel.rmq.events.queue_declarer import register_rmq_queue_declare_handler
from src.kernel.rmq.events.runner import register_rmq_handler

event_handlers = [
    # Persistence
    register_init_pools_handler,
    register_postgres_handler,

    # RMQ Handlers
    register_rmq_exchange_declare_handler,
    register_rmq_queue_declare_handler,
    register_rmq_bind_handler,
    register_rmq_handler,

]


def set_event_handlers(application: FastAPI, app_settings: AppSettings) -> FastAPI:
    json_logger = get_json_logger()

    for event_handler in event_handlers:
        event_handler(application, app_settings, json_logger)

    return application
