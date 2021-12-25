import uuid
from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from models.base import BaseModel

from services.genre import GenreService, get_genre_service
from services.utils import get_params

router = APIRouter()


class Genre(BaseModel):
    uuid: uuid.UUID
    name: str
    description: Optional[str]


@router.get('/search', response_model=list[Genre])
@router.get('', response_model=list[Genre])
async def genres_list(request: Request, genre_service: GenreService = Depends(get_genre_service)) -> list[Genre]:
    params = get_params(request)
    genres = await genre_service.get_by_params(**params)
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genres not found')
    return [
        Genre(
            uuid=genre.id,
            name=genre.name,
            description=genre.description,
        ) for genre in genres
    ]


@router.get('/{genre_id}', response_model=Genre)
async def genre_details(genre_id: str, genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
    return Genre(
        uuid=genre.id,
        name=genre.name,
        description=genre.description,
    )
