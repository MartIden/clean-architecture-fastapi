from typing import Any

from pydantic import BaseModel


def convert_field_to_camel_case(string: str) -> str:
    return "".join(
        word if index == 0 else word.capitalize()
        for index, word in enumerate(string.split("_"))
    )


class BaseDto(BaseModel):
    class Config:
        frozen = True


class JsonDto(BaseModel):
    class Config:
        frozen = True
        populate_by_name = True
        alias_generator = convert_field_to_camel_case


class JsonRequest(JsonDto):
    pass


class JsonResponse(JsonDto):
    success: bool
    answer: Any | None = None
    error: Any | None = None
