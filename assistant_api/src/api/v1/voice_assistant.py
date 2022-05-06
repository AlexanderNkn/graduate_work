from http import HTTPStatus

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from fastapi.responses import HTMLResponse

# from core.messages import RE
from dependencies.authentication import get_token, make_request
from dependencies.movies import make_request as movies_make_request
# from models.genre import GenreDetailedResponse
# from services.genre import GenreService, get_genre_service
from services.utils import get_site

router = APIRouter()


async def check_film_list_permission(token=get_token(), x_request_id=Header(None)):
    await make_request(permission='film', token=token, x_request_id=x_request_id)


async def check_film_detail_permission(token=get_token(), x_request_id=Header(None)):
    await make_request(permission='film', token=token, x_request_id=x_request_id)


async def get_film_list(query, token, x_request_id):
    return await movies_make_request(data_type='film', query=query, token=token, x_request_id=x_request_id)


async def get_genre_list(query, token, x_request_id):
    return await movies_make_request(data_type='genre', query=query, token=token, x_request_id=x_request_id)


async def get_person_list(query, token, x_request_id):
    return await movies_make_request(data_type='person', query=query, token=token, x_request_id=x_request_id)


@router.get(
    '/search',
    # response_model=list[GenreDetailedResponse],
    summary='Search by films',
    description='List of films',
    response_description='List of films',
)
async def voice_query(
    request: Request,
    query: str = None,
    response_class=HTMLResponse,
    # genre_service: GenreService = Depends(get_genre_service),
    # allowed: bool = Depends(check_genre_list_permission),
    token=get_token(),
    x_request_id=Header(None)
) -> HTMLResponse:
    films = await get_film_list(query, token, x_request_id)
    genres = await get_genre_list(query, token, x_request_id)
    persons = await get_person_list(query, token, x_request_id)
    html_content = get_site('templates/index.html', query, films=films, genres=genres, persons=persons)
    return HTMLResponse(content=html_content, status_code=200)
