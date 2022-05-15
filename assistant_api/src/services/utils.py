import os

import aiohttp
import pybreaker
from fastapi import HTTPException, status
from jinja2 import Environment, FileSystemLoader

from core.config import settings

# db_breaker is an implementation of Circuit Breaker algorithm
db_breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60)


@db_breaker(__pybreaker_call_async=True)
async def make_post_request(url: str, payload: dict, headers: dict) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, json=payload, headers=headers) as response:
            if response.status != status.HTTP_200_OK:
                raise HTTPException(status_code=response.status)


@db_breaker(__pybreaker_call_async=True)
async def make_get_request(url: str, headers: dict) -> aiohttp.ClientResponse | None:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as response:
            if response.status == status.HTTP_200_OK:
                return await response.json()
            elif response.status == status.HTTP_404_NOT_FOUND:
                return None
            raise HTTPException(status_code=response.status)


def get_site(data: dict, template_path: str) -> str:
    """Returns rendered html."""
    template_dir = os.path.join(settings.base_dir, 'templates')
    template_loader = FileSystemLoader(template_dir)
    env = Environment(loader=template_loader, autoescape=True)

    template = env.get_template(template_path)
    return template.render(**data)
