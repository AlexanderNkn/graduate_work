import aiohttp
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import pybreaker
from http import HTTPStatus

from core import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='', auto_error=config.ENABLE_AUTHORIZATION)
db_breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60)


def get_token(token: str = Depends(oauth2_scheme)):
    return token


# db_breaker is an implementation of Circuit Breaker algorithm
@db_breaker(__pybreaker_call_async=True)
async def make_request(data_type: str, query: str, token: str, x_request_id: str):
    async with aiohttp.ClientSession() as session:
        url = f'{config.MOVIESAPI_HOST}:{config.MOVIESAPI_PORT}{config.MOVIESAPI_BASE_URL}/{data_type}'
        url += f'?query={query}'
        async with session.get(
            url=url,
            json={},
            headers={
                # 'Authorization': f'Bearer {token}',
                # 'X-Request-Id': x_request_id,
            },
        ) as response:
            data = await response.json()
            status = response.status
            if status == HTTPStatus.NOT_FOUND:
                return []
            return data
            # if data['status'] == 'error' or (data['status'] == 'success' and data['has_permission'] is False):
            #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=data)
