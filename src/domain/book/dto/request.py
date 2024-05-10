from src.domain.book.value_obj.description import Description
from src.domain.book.value_obj.isbn import Isbn
from src.domain.book.value_obj.title import Title
from src.domain.common.dto import JsonRequest
from src.domain.common.value_obj.id import Id


class NewBookRequest(JsonRequest):
    title: Title
    description: Description
    isbn: Isbn
    author_id: Id


class UpdateBookRequest(JsonRequest):
    id: Id

    title: Title | None = None
    description: Description | None = None
    isbn: Isbn | None = None
    author_id: Id | None = None
