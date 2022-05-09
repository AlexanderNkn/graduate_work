from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from core import config
from services.utils import make_post_request

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='', auto_error=config.ENABLE_AUTHORIZATION)


def get_token(token: str = Depends(oauth2_scheme)):
    return token


async def make_auth_request(permission: str, token: str, x_request_id: str):
    headers = {'X-Request-Id': x_request_id}
    if not config.ENABLE_AUTHORIZATION:
        return headers

    headers.update({'Authorization': f'Bearer {token}'})
    url = f'{config.AUTH_HOST}:{config.AUTH_PORT}{config.AUTH_BASE_URL}/check-permission'
    payload = {'permission': f'{permission}'}
    make_post_request(url, payload, headers)
    return headers
