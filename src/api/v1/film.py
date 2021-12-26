from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from models.film import FilmShortResponse, FilmDetailedResponse
from models.genre import GenreShortResponse
from models.person import PersonShortResponse

from services.film import FilmService, get_film_service
from services.utils import get_params

router = APIRouter()


@router.get('/search', response_model=list[FilmShortResponse])
@router.get('', response_model=list[FilmShortResponse])
async def films_list(request: Request, film_service: FilmService = Depends(get_film_service)) -> list[FilmShortResponse]:
    params = get_params(request)
    film_list = await film_service.get_by_params(**params)
    if not film_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return [
        FilmShortResponse(
            uuid=film.id,
            title=film.title,
            imdb_rating=film.imdb_rating,
        ) for film in film_list
    ]


@router.get('/{film_id}', response_model=FilmDetailedResponse)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> FilmDetailedResponse:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return FilmDetailedResponse(
        uuid=film.id,
        title=film.title,
        imdb_rating=film.imdb_rating,
        description=film.description,
        genre=[GenreShortResponse(uuid=genre.id, name=genre.name) for genre in film.genre],
        actors=[PersonShortResponse(uuid=actor.id, full_name=actor.name) for actor in film.actors],
        writers=[PersonShortResponse(uuid=writer.id, full_name=writer.name) for writer in film.writers],
        directors=[PersonShortResponse(uuid=director.id, full_name=director.name) for director in film.directors],
    )
