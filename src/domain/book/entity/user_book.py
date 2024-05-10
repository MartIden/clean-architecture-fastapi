from src.domain.common.entity import Entity
from src.domain.common.value_obj.id import Id


class UserBook(Entity):
    user_id: Id
    book_id: Id
