import uuid
from typing import Optional

from .base import BaseModel


class GenreShortResponse(BaseModel):
    """Genre with name, without details."""
    uuid: uuid.UUID
    name: str


class GenreDetailedResponse(BaseModel):
    """Genre details with name and description."""
    uuid: uuid.UUID
    name: str
    description: Optional[str]


class GenreShortDTO(BaseModel):
    """Genre id and name received from elasticsearch."""
    id: uuid.UUID
    name: str


class GenreDetailedDTO(BaseModel):
    """Genre details received from elasticsearch."""
    id: uuid.UUID
    name: str
    description: Optional[str]
