from fastapi import APIRouter, Depends, Header
from fastapi.responses import ORJSONResponse

from dependencies.authentication import get_token, make_auth_request
from services.handlers import get_handler
from services.intent import get_intent, ParsedQuery

router = APIRouter()


async def check_voice_permission(token=get_token(), x_request_id=Header(None)):
    return await make_auth_request(permission='voice', token=token, x_request_id=x_request_id)


@router.get(
    '/search',
    response_class=ORJSONResponse,
    summary='List of suitable films and persons',
    description='List of suitable films and persons data returned by voice search',
    response_description='List of films and persons data',
)
async def voice_query(
    query: str | None = None,
    authorized_headers: dict = Depends(check_voice_permission),
) -> dict:
    parsed_query: ParsedQuery = get_intent(query)
    handler = get_handler(parsed_query.intent)
    answer = await handler(headers=authorized_headers, params=parsed_query.params)
    # TODO json response for testing purposes. It should be replaced with html
    return {'answer': answer}
