import uvicorn
from fastapi import FastAPI


__all__ = ["app"]

from src.kernel.fastapi.config import get_app_settings
from src.kernel.fastapi.registration.event_handlers import set_event_handlers
from src.kernel.fastapi.registration.exception_handlers import set_exception_handlers
from src.kernel.fastapi.registration.middlewares import set_middlewares
from src.kernel.fastapi.registration.urls import set_routers


def get_application() -> FastAPI:

    app_settings = get_app_settings()
    application = FastAPI(**app_settings.fastapi_kwargs)

    set_exception_handlers(application)
    set_event_handlers(application, app_settings)
    set_middlewares(application, app_settings)
    set_routers(application, app_settings)

    return application


app = get_application()


if __name__ == "__main__":
    uvicorn.run("src.kernel.fastapi.run:app", host="0.0.0.0", port=5005, reload=True, log_level=30)
