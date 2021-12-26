import uuid as uuid

from .base import BaseModel


class PersonShortResponse(BaseModel):
    """Person with name, without details."""
    uuid: uuid.UUID
    full_name: str


class PersonDetailedResponse(BaseModel):
    """Genre details with full_name, role and film_ids."""
    uuid: uuid.UUID
    full_name: str
    role: list[str]
    film_ids: list[uuid.UUID]


class PersonShortDTO(BaseModel):
    """Person id and name received from elasticsearch."""
    id: uuid.UUID
    name: str


class PersonDetailedDTO(BaseModel):
    """Person details received from elasticsearch."""
    id: uuid.UUID
    full_name: str
    role: list[str]
    film_ids: list[uuid.UUID]
