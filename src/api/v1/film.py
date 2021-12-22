import uuid
from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services.film import FilmService, get_film_service

router = APIRouter()


class PersonName(BaseModel):
    uuid: uuid.UUID
    name: str


class Film(BaseModel):
    uuid: uuid.UUID
    imdb_rating: float
    genre: list[str]
    title: str
    description: str
    director: Optional[list[str]]
    actors_names: Optional[list[str]]
    writers_names: Optional[list[str]]
    actors: list[PersonName]
    writers: list[PersonName]


@router.get('/{film_id}', response_model=Film)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return Film(
        uuid=film.id,
        imdb_rating=film.imdb_rating,
        genre=film.genre,
        title=film.title,
        description=film.description,
        director=film.director,
        actors_names=film.actors_names,
        writers_names=film.writers_names,
        actors=[PersonName(uuid=actor.id, name=actor.name) for actor in film.actors],
        writers=[PersonName(uuid=writer.id, name=writer.name) for writer in film.writers],
    )
