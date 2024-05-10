from pydantic import BaseModel

from src.domain.author.value_obj.name import Name
from src.domain.author.value_obj.surname import Surname


class NewAuthor(BaseModel):
    name: Name
    surname: Surname
