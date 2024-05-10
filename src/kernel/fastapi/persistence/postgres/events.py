from logging import Logger

from fastapi import FastAPI

from src.kernel.fastapi.persistence.postgres.create_connection import run_postgres_db
from src.kernel.fastapi.settings.app import AppSettings


def register_postgres_handler(
    application: FastAPI, app_settings: AppSettings, json_logger: Logger
) -> None:
    application.add_event_handler("startup", run_postgres_db(application, app_settings))
