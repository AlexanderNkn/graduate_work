import uuid
from typing import Optional

from .base import BaseModel


class GenreShortResponse(BaseModel):
    uuid: uuid.UUID
    name: str


class GenreDetailedResponse(BaseModel):
    uuid: uuid.UUID
    name: str
    description: Optional[str]


class GenreShortDTO(BaseModel):
    id: uuid.UUID
    name: str


class GenreDetailedDTO(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str]
