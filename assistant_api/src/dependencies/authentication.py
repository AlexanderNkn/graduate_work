from hashlib import sha1

from fastapi import Depends, Header, Request
from fastapi.security import OAuth2PasswordBearer

from core.config import settings
from services.utils import make_post_request

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='', auto_error=settings.enable_authorization)


def get_token(token: str = Depends(oauth2_scheme)):
    return token


def get_user_identity(request: Request, user_agent: str | None = Header(default=None)) -> str:
    ip = request.client.host
    return sha1((ip + user_agent).encode(), usedforsecurity=False).hexdigest()


async def make_auth_request(permission: str, token: str, x_request_id: str):
    headers = {'X-Request-Id': x_request_id}
    if not settings.enable_authorization:
        return headers

    headers.update({'Authorization': f'Bearer {token}'})
    url = f'{settings.auth_host}:{settings.auth_port}{settings.auth_base_url}/check-permission'
    payload = {'permission': f'{permission}'}
    make_post_request(url, payload, headers)
    return headers
