from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from models.film import FilmShortResponse
from models.person import PersonDetailedResponse

from services.person import PersonService, get_person_service
from services.film import FilmService, get_film_service
from services.utils import get_params

router = APIRouter()


@router.get('/search', response_model=list[PersonDetailedResponse])
@router.get('', response_model=list[PersonDetailedResponse])
async def persons_list(request: Request,
                       person_service: PersonService = Depends(get_person_service)) -> list[PersonDetailedResponse]:
    params = get_params(request)
    person_list = await person_service.get_by_params(**params)
    if not person_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return [
        PersonDetailedResponse(
            uuid=person.id,
            full_name=person.full_name,
            role=person.role,
            film_ids=person.film_ids,
        ) for person in person_list
    ]


@router.get('/{person_id}/film/', response_model=list[FilmShortResponse])
async def person_film(person_id: str,
                      request: Request,
                      person_service: PersonService = Depends(get_person_service),
                      film_service: FilmService = Depends(get_film_service)) -> list[FilmShortResponse]:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    params = get_params(request)
    params.setdefault('should', []).extend([{'id': str(film_id)} for film_id in person.film_ids])
    film_list = await film_service.get_by_params(**params)

    return [
        FilmShortResponse(
            uuid=film.id,
            title=film.title,
            imdb_rating=film.imdb_rating,
        ) for film in film_list
    ]


@router.get('/{person_id}', response_model=PersonDetailedResponse)
async def person_details(person_id: str,
                         person_service: PersonService = Depends(get_person_service)) -> PersonDetailedResponse:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return PersonDetailedResponse(
        uuid=person.id,
        full_name=person.full_name,
        role=person.role,
        film_ids=person.film_ids,
    )
