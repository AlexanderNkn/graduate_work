import uuid
from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from services.person import PersonService, get_person_service
from services.utils import get_params

router = APIRouter()


class Person(BaseModel):
    uuid: uuid.UUID
    full_name: str
    role: list[str]
    film_ids: list[uuid.UUID]


@router.get('/{person_id}', response_model=Person)
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)) -> Person:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return Person(
        uuid=person.id,
        full_name=person.full_name,
        role=person.role,
        film_ids=person.film_ids,
    )


@router.get('', response_model=list[Person])
async def persons_list(request: Request, person_service: PersonService = Depends(get_person_service)) -> list[Person]:
    params = get_params(request)
    person_list = await person_service.get_persons_by_params(**params)
    if not person_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return [
        Person(
            uuid=person.id,
            full_name=person.full_name,
            role=person.role,
            film_ids=person.film_ids,
        ) for person in person_list
    ]
