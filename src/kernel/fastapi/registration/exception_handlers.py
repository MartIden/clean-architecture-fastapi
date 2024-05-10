from dataclasses import dataclass
from typing import Callable, Type

import redis
from aiohttp import ClientConnectorError
from asyncpg import PostgresError, UniqueViolationError
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from src.domain.user.exceptions.token import IncorrectAuthToken
from src.kernel.fastapi.exceptions.handlers.base import http_error_handler, \
    http_validation_error_handler, http_business_error_handler


@dataclass
class FastapiExceptionHandler:
    exception_type: Type[Exception]
    exception_handler: Callable


exception_handlers = [
    FastapiExceptionHandler(Exception, http_error_handler),
    FastapiExceptionHandler(AttributeError, http_error_handler),
    FastapiExceptionHandler(TypeError, http_error_handler),
    FastapiExceptionHandler(ValueError, http_error_handler),
    FastapiExceptionHandler(IndexError, http_error_handler),
    FastapiExceptionHandler(KeyError, http_error_handler),
    FastapiExceptionHandler(EOFError, http_error_handler),
    FastapiExceptionHandler(ConnectionRefusedError, http_error_handler),
    FastapiExceptionHandler(redis.exceptions.ConnectionError, http_error_handler),
    FastapiExceptionHandler(UniqueViolationError, http_business_error_handler),
    FastapiExceptionHandler(ValidationError, http_validation_error_handler),
    FastapiExceptionHandler(ClientConnectorError, http_error_handler),
    FastapiExceptionHandler(RequestValidationError, http_validation_error_handler),
    FastapiExceptionHandler(PostgresError, http_error_handler),
    FastapiExceptionHandler(IncorrectAuthToken, http_error_handler),
]


def set_exception_handlers(application: FastAPI) -> FastAPI:
    for exc_handler in exception_handlers:
        application.add_exception_handler(
            exc_handler.exception_type, exc_handler.exception_handler
        )

    return application
