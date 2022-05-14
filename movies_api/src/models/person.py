from typing import Optional
from uuid import UUID

from .base import BaseModel


class PersonShortResponse(BaseModel):
    """Person with name, without details."""

    uuid: UUID
    full_name: str


class PersonDetailedResponse(BaseModel):
    """Genre details with full_name, role and film_ids."""

    uuid: UUID
    full_name: str
    role: list[str]
    film_ids: list[UUID]


class PersonShortDTO(BaseModel):
    """Person id and name received from elasticsearch."""

    id: UUID
    name: str
    photo_path: Optional[str]


class PersonDetailedDTO(BaseModel):
    """Person details received from elasticsearch."""

    id: UUID
    full_name: str
    role: list[str]
    film_ids: list[UUID]
