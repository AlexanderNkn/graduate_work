from fastapi import APIRouter, Depends, Header, status
from fastapi.responses import HTMLResponse

from core.messages import REQUEST_NOT_UNDERSTAND
from dependencies.authentication import get_token, make_auth_request
from db.redis_db import get_redis
from services.handlers import get_handler
from services.intent import get_intent, ParsedQuery
from services.utils import get_site

router = APIRouter()


async def check_voice_permission(token=get_token(), x_request_id=Header(None)):
    return await make_auth_request(permission='voice', token=token, x_request_id=x_request_id)


@router.get(
    '/search',
    response_class=HTMLResponse,
    summary='List of suitable films and persons',
    description='List of suitable films and persons data returned by voice search',
    response_description='List of films and persons data',
)
async def voice_query(
    query: str | None = None,
    authorized_headers: dict = Depends(check_voice_permission),
    cache=Depends(get_redis),
) -> HTMLResponse:
    data = {}
    if query is not None:
        parsed_query: ParsedQuery = get_intent(query)
        if parsed_query is not None:
            handler = get_handler(parsed_query.intent)
            data = await handler(authorized_headers, parsed_query, cache)
        else:
            data = {'text_to_speech': REQUEST_NOT_UNDERSTAND}
    html_content = get_site(data, 'index.html')
    return HTMLResponse(content=html_content, status_code=status.HTTP_200_OK)


@router.get(
    '/demo',
    response_class=HTMLResponse,
    summary='List of questions for demo',
    description='List of questions for demo',
    response_description='List of questions for demo',
)
async def get_demo(
) -> HTMLResponse:
    html_content = get_site({}, 'questions_list.html')
    return HTMLResponse(content=html_content, status_code=status.HTTP_200_OK)
