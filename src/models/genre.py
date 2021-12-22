import uuid

from .base import BaseModel


class Genre(BaseModel):
    id: uuid.UUID
    name: str
    description: str
