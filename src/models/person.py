import uuid

from .base import BaseModel


class Person(BaseModel):
    id: uuid.UUID
    full_name: str
    role: list[str]
    film_ids: list[uuid.UUID]
