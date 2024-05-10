import secrets
from typing import Annotated

from fastapi import Depends, status, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.adapters.input.http.depends.keycloak_token_getter import get_token_user
from src.infrastructure.config.base import get_app_settings
from src.infrastructure.settings.fastapi.app import AppSettings

security = HTTPBasic()


def get_current_doc_auth_username(
    credentials: HTTPBasicCredentials = Depends(security),
    settings: AppSettings = Depends(get_app_settings)
):
    get_token_user()

    username = "login"
    password = "pass"
    correct_username = secrets.compare_digest(credentials.username, username)
    correct_password = secrets.compare_digest(credentials.password, password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
