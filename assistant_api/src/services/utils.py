import aiohttp
import pybreaker

from fastapi import HTTPException, status

db_breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60)


# db_breaker is an implementation of Circuit Breaker algorithm
@db_breaker(__pybreaker_call_async=True)
async def make_post_request(url: str, payload: dict, headers: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, json=payload, headers=headers) as response:
            if response.status != status.HTTP_200_OK:
                raise HTTPException(status_code=response.status)


@db_breaker(__pybreaker_call_async=True)
async def make_get_request(url: str, headers: dict):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as response:
            if response.status != status.HTTP_200_OK:
                raise HTTPException(status_code=response.status)
            return await response.json()
