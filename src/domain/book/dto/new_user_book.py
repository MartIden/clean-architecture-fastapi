from pydantic import BaseModel

from src.domain.common.value_obj.id import Id


class NewUserBook(BaseModel):
    user_id: Id
    book_id: Id
