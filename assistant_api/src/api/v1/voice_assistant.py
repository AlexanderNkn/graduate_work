from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.responses import HTMLResponse

from core.messages import REQUEST_NOT_UNDERSTAND
from dependencies.authentication import get_token, make_auth_request
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
) -> HTMLResponse:
    data = {}
    if query is not None:
        parsed_query: ParsedQuery = get_intent(query)
        if parsed_query is None:
            data = {'text_to_speech': REQUEST_NOT_UNDERSTAND}
        else:
            handler = get_handler(parsed_query.intent)
            data = await handler(headers=authorized_headers, params=parsed_query.params)
    html_content = get_site(data, 'index.html')
    return HTMLResponse(content=html_content, status_code=status.HTTP_200_OK)
