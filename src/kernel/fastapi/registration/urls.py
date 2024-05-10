from fastapi import FastAPI, Depends
from starlette_exporter import PrometheusMiddleware, handle_metrics

from src.kernel.fastapi.middlwares.request_logging_middleware import RequestJSONLoggerMiddleware
from src.kernel.fastapi.routers.versions.v1.api import client_router
from src.kernel.fastapi.routers.versions.v1.docs import docs_router
from src.kernel.fastapi.routers.versions.v1.webhook import webhook_router
from src.kernel.fastapi.settings.app import AppSettings


def set_routers(application: FastAPI, app_settings: AppSettings) -> FastAPI:
    application.include_router(
        client_router,
        dependencies=[Depends(RequestJSONLoggerMiddleware.log_middle)],
    )
    application.include_router(
        webhook_router,
        dependencies=[Depends(RequestJSONLoggerMiddleware.log_middle)],
    )
    application.include_router(
        docs_router,
        dependencies=[Depends(RequestJSONLoggerMiddleware.log_middle)],
    )

    """Prometheus metrics"""
    application.add_middleware(
        PrometheusMiddleware,
        app_name="support_portal",
        prefix="support_portal"
    )
    application.add_route("/metrics", handle_metrics)

    return application
