import uuid as uuid

from .base import BaseModel


class PersonShortResponse(BaseModel):
    uuid: uuid.UUID
    full_name: str


class PersonDetailedResponse(BaseModel):
    uuid: uuid.UUID
    full_name: str
    role: list[str]
    film_ids: list[uuid.UUID]


class PersonShortDTO(BaseModel):
    id: uuid.UUID
    name: str


class PersonDetailedDTO(BaseModel):
    id: uuid.UUID
    full_name: str
    role: list[str]
    film_ids: list[uuid.UUID]
