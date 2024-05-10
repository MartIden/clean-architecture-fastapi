from fastapi import APIRouter, Depends
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from starlette.requests import Request

from src.kernel.fastapi.config import get_app_settings
from src.kernel.fastapi.settings.app import AppSettings
from src.presentation.http.depends.basic_auth_validator import basic_auth_validate

docs_api = APIRouter(prefix="/docs", tags=["docs"])


@docs_api.get("/", include_in_schema=False)
async def get_swagger_documentation(_=Depends(basic_auth_validate)):
    return get_swagger_ui_html(openapi_url="/docs/openapi.json", title="docs")


@docs_api.get("/redoc", include_in_schema=False)
async def get_redoc_documentation(_=Depends(basic_auth_validate)):
    return get_redoc_html(openapi_url="/docs/openapi.json", title="docs")


@docs_api.get("/openapi.json", include_in_schema=False)
async def openapi(
    request: Request,
    settings: AppSettings = Depends(get_app_settings),
    _=Depends(basic_auth_validate)
):
    return get_openapi(title=settings.TITLE, version=settings.VERSION, routes=request.app.routes)
