from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette import status

from src.kernel.fastapi.config import get_app_settings
from src.kernel.fastapi.settings.app import AppSettings


def basic_auth_validate(
    credentials: Annotated[HTTPBasicCredentials, Depends(HTTPBasic())],
    app_settings: AppSettings = Depends(get_app_settings)
) -> None:

    if not all((
        app_settings.DOC_LOGIN == credentials.username,
        app_settings.DOC_PASS == credentials.password,
    )):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Basic"},
        )
