import uuid
from http import HTTPStatus
import elasticsearch

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from services.film import FilmService, get_film_service
from services.utils import get_params

router = APIRouter()


class PersonName(BaseModel):
    uuid: uuid.UUID
    name: str


class Genre(BaseModel):
    uuid: uuid.UUID
    name: str


class FilmDetailed(BaseModel):
    uuid: uuid.UUID
    title: str
    imdb_rating: float
    description: str
    genre: list[Genre]
    actors: list[PersonName]
    writers: list[PersonName]
    directors: list[PersonName]


class FilmShort(BaseModel):
    uuid: uuid.UUID
    imdb_rating: float
    title: str


@router.get('/search', response_model=list[FilmShort])
@router.get('', response_model=list[FilmShort])
async def films_list(request: Request, film_service: FilmService = Depends(get_film_service)) -> list[FilmShort]:
    params = get_params(request)
    film_list = await film_service.get_by_params(**params)
    if not film_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return [
        FilmShort(
            uuid=film.id,
            title=film.title,
            imdb_rating=film.imdb_rating,
        ) for film in film_list
    ]


@router.get('/{film_id}', response_model=FilmDetailed)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> FilmDetailed:
    try:
        film = await film_service.get_by_id(film_id)
    except elasticsearch.exceptions.NotFoundError:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return FilmDetailed(
        uuid=film.id,
        title=film.title,
        imdb_rating=film.imdb_rating,
        description=film.description,
        genre=[Genre(uuid=genre.id, name=genre.name) for genre in film.genre],
        actors=[PersonName(uuid=actor.id, name=actor.name) for actor in film.actors],
        writers=[PersonName(uuid=writer.id, name=writer.name) for writer in film.writers],
        directors=[PersonName(uuid=director.id, name=director.name) for director in film.directors],
    )
