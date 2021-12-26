import uuid
from typing import Optional

from .base import BaseModel
from .genre import GenreShortResponse, GenreShortDTO
from .person import PersonShortResponse, PersonShortDTO


class FilmShortResponse(BaseModel):
    uuid: uuid.UUID
    imdb_rating: float
    title: str


class FilmDetailedResponse(BaseModel):
    uuid: uuid.UUID
    title: str
    imdb_rating: float
    description: Optional[str]
    genre: list[GenreShortResponse]
    actors: list[PersonShortResponse]
    writers: list[PersonShortResponse]
    directors: list[PersonShortResponse]


class FilmDetailedDTO(BaseModel):
    id: uuid.UUID
    imdb_rating: float
    genre: list[GenreShortDTO]
    title: str
    description: Optional[str]
    actors_names: Optional[list[str]]
    writers_names: Optional[list[str]]
    directors_names: Optional[list[str]]
    actors: list[PersonShortDTO]
    writers: list[PersonShortDTO]
    directors: list[PersonShortDTO]
