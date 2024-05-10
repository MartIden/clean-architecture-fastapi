from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware

from src.kernel.fastapi.settings.app import AppSettings


def set_middlewares(application: FastAPI, app_settings: AppSettings) -> FastAPI:
    application.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.ALLOWED_HOSTS,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_middleware(
        RawContextMiddleware,
        plugins=(
            plugins.RequestIdPlugin(),
            plugins.CorrelationIdPlugin(),
            plugins.ForwardedForPlugin(),
            plugins.UserAgentPlugin()
        ),
    )

    return application
