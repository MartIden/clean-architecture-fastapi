from src.domain.author.value_obj.name import Name
from src.domain.author.value_obj.surname import Surname
from src.domain.common.entity import Entity


class Author(Entity):
    name: Name
    surname: Surname
