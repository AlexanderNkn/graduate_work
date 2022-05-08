from http import HTTPStatus

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from fastapi.responses import ORJSONResponse

from core.messages import REQUEST_NOT_UNDERSTAND
from dependencies.authentication import get_token, make_request

router = APIRouter()


async def check_voice_permission(token=get_token(), x_request_id=Header(None)):
    await make_request(permission='voice', token=token, x_request_id=x_request_id)


@router.get(
    '/search',
    response_class=ORJSONResponse,
    summary='List of suitable films and persons',
    description='List of suitable films and persons data returned by voice search',
    response_description='List of films and persons data',
)
async def films_list(
    request: Request,
    allowed: bool = Depends(check_voice_permission),
) -> dict:
    # TODO json response for testing purposes. It should be replaced with html
    return {"message": "Hello World"}
