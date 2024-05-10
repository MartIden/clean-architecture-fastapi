from src.domain.book.value_obj.description import Description
from src.domain.book.value_obj.isbn import Isbn
from src.domain.book.value_obj.title import Title
from src.domain.common.dto import JsonDto, JsonResponse
from src.domain.common.value_obj.created_at import CreatedAt
from src.domain.common.value_obj.id import Id
from src.domain.common.value_obj.updated_at import UpdatedAt


class BookOut(JsonDto):
    id: Id

    title: Title
    description: Description
    isbn: Isbn
    author_id: Id

    created_at: CreatedAt
    updated_at: UpdatedAt


class BookJsonResponse(JsonResponse):
    answer: BookOut | None = None


class BooksWrapper(JsonDto):
    entities: list[BookOut] | None = None
    count: int


class BooksJsonResponse(JsonResponse):
    answer: BooksWrapper | None = None
