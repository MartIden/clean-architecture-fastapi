from pydantic import BaseModel

from src.domain.common.value_obj.id import Id
from src.domain.common.value_obj.created_at import CreatedAt
from src.domain.common.value_obj.updated_at import UpdatedAt


class Entity(BaseModel):
    id: Id
    created_at: CreatedAt
    updated_at: UpdatedAt
