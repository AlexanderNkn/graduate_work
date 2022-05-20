"""Module contains methods for fetching data from movies_api with further processing."""
from collections.abc import Callable, Coroutine

import orjson

from core import messages
from core.config import settings
from db.redis_db import RedisStorage
from services.intent import ParsedQuery

from .utils import make_get_request

# The common url for all requests to movies api
URL = f'{settings.movies_host}:{settings.movies_port}{settings.movies_base_url}'


def get_handler(intent: str) -> Callable[..., Coroutine[None, None, dict]]:
    """Maps intent with its method."""
    return {
        'director_search': get_director,
        'actor_search': get_actor,
        'writer_search': get_writer,
        'duration_search': get_duration,
        'film_by_person': get_film_by_person,
        'other_films': get_another_film,
    }[intent]


async def _search(headers, query: ParsedQuery, cache: RedisStorage):
    if query.check_cache:
        cached_data = await cache.get()
        return cached_data and orjson.loads(cached_data)

    params = query.params
    fields = ','.join(params.keys())
    values = ' '.join(params.values())
    url = f'{URL}/film/search?query[{fields}]={values}&all=true'
    response = await make_get_request(url, headers)
    await cache.set(orjson.dumps(response))
    return response


async def get_director(headers, query: ParsedQuery, cache: RedisStorage) -> dict:
    data = await _search(headers, query, cache)
    directors_names = data and data[0].get('directors_names')
    if directors_names is None:
        return {'text_to_speech': messages.NOT_FOUND}
    return {
        'text_to_speech': f'Режиссер фильма {", ".join(directors_names)}',
        'persons': data[0]['directors'],
    }


async def get_actor(headers, query: ParsedQuery, cache: RedisStorage) -> dict:
    data = await _search(headers, query, cache)
    actors_names = data and data[0].get('actors_names')
    if actors_names is None:
        return {'text_to_speech': messages.NOT_FOUND}
    return {
        'text_to_speech': f'Актеры фильма {", ".join(actors_names)}',
        'persons': data[0]['actors'],
    }


async def get_writer(headers, query: ParsedQuery, cache: RedisStorage) -> dict:
    data = await _search(headers, query, cache)
    writers_names = data and data[0].get('writers_names')
    if writers_names is None:
        return {'text_to_speech': messages.NOT_FOUND}
    return {
        'text_to_speech': f'Сценарист фильма {", ".join(writers_names)}',
        'persons': data[0]['writers'],
    }


async def get_duration(headers, query: ParsedQuery, cache: RedisStorage) -> dict:
    data = await _search(headers, query, cache)
    duration = data and data[0].get('duration')
    if data is None:
        return {'text_to_speech': messages.NOT_FOUND}
    return {'text_to_speech': f'Длительность фильма {duration} минут'}


async def get_film_by_person(headers, query: ParsedQuery, cache: RedisStorage) -> dict:
    data = await _search(headers, query, cache)
    if data is None:
        return {'text_to_speech': messages.NOT_FOUND}

    titles = ', '.join(film_data['title'] for film_data in data)
    return {
        'text_to_speech': f'Всего фильмов {len(data)}. Это - {titles}',
        'films': data,
    }


async def get_another_film(headers, query: ParsedQuery, cache: RedisStorage) -> dict:
    cached_data = await cache.get()
    if cached_data is not None:
        if not query.context_role:
            query.context_role = 'directors_names'
        person_names = orjson.loads(cached_data)[0].get(query.context_role)
        query.params = {
            query.context_role: ' '.join(person_names),
        }
        data = await _search(headers, query, cache)

    if data is not None:
        titles = ', '.join(film_data['title'] for film_data in data)
        return {
            'text_to_speech': f'Всего фильмов {len(data)}. Это - {titles}',
            'films': data,
        }

    return {'text_to_speech': messages.NOT_FOUND}
