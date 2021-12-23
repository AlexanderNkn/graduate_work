import uuid
from http import HTTPStatus
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from services.genre import GenreService, get_genre_service

router = APIRouter()


class Genre(BaseModel):
    uuid: uuid.UUID
    name: str
    description: Optional[str]


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


@router.get('', response_model=List[Genre])
async def genre_list(genre_service: GenreService = Depends(get_genre_service)) -> List[Genre]:
    genres = await genre_service.get_genre_list()
    return [
        Genre(uuid=genre.id,
              name=genre.name,
              description=genre.description,
              )
        for genre in genres]
