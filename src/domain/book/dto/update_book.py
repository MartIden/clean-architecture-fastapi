from pydantic import BaseModel

from src.domain.book.value_obj.description import Description
from src.domain.book.value_obj.isbn import Isbn
from src.domain.book.value_obj.title import Title
from src.domain.common.value_obj.id import Id


class UpdateBook(BaseModel):
    id: Id

    title: Title | None = None
    description: Description | None = None
    isbn: Isbn | None = None
    author_id: Id | None = None
