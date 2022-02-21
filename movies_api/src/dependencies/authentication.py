import aiohttp
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='', auto_error=config.ENABLE_AUTHORIZATION)


def get_token(token: str = Depends(oauth2_scheme)):
    return token


async def make_request(permission: str, token: str):
    if not config.ENABLE_AUTHORIZATION:
        return
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=f'http://{config.AUTH_HOST}:{config.AUTH_PORT}{config.AUTH_BASE_URL}/check-permission',
            json={'permission': f'{permission}'},
            headers={'Authorization': f'Bearer {token}'},
        ) as response:
            data = await response.json()
            if data['status'] == 'error' or (data['status'] == 'success' and data['has_permission'] is False):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=data)
