from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from models.genre import GenreDetailedResponse

from services.genre import GenreService, get_genre_service
from services.utils import get_params

router = APIRouter()


@router.get('/search', response_model=list[GenreDetailedResponse])
@router.get('', response_model=list[GenreDetailedResponse])
async def genres_list(request: Request,
                      genre_service: GenreService = Depends(get_genre_service)) -> list[GenreDetailedResponse]:
    params = get_params(request)
    genres = await genre_service.get_by_params(**params)
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genres not found')
    return [
        GenreDetailedResponse(
            uuid=genre.id,
            name=genre.name,
            description=genre.description,
        ) for genre in genres
    ]


@router.get('/{genre_id}', response_model=GenreDetailedResponse)
async def genre_details(genre_id: str,
                        genre_service: GenreService = Depends(get_genre_service)) -> GenreDetailedResponse:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
    return GenreDetailedResponse(
        uuid=genre.id,
        name=genre.name,
        description=genre.description,
    )
