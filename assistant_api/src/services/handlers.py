"""Module contains methods for fetching data from movies_api with further processing."""
from collections.abc import Callable, Coroutine

from core import messages
from core.config import settings

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
    }[intent]


async def _search(params, headers):
    fields = ','.join(params.keys())
    values = ' '.join(params.values())
    url = f'{URL}/film/search?query[{fields}]={values}&all=true'
    return await make_get_request(url, headers)


async def get_director(headers, params) -> dict:
    data = await _search(params, headers)
    directors_names = data and data[0].get('directors_names')
    if directors_names is None:
        return {'text_to_speech': messages.NOT_FOUND}
    return {
        'text_to_speech': f'Режиссер фильма {", ".join(directors_names)}',
        'persons': data[0]['directors'],
    }


async def get_actor(headers, params) -> dict:
    data = await _search(params, headers)
    actors_names = data and data[0].get('actors_names')
    if actors_names is None:
        return {'text_to_speech': messages.NOT_FOUND}
    return {
        'text_to_speech': f'Актеры фильма {", ".join(actors_names)}',
        'persons': data[0]['actors'],
    }


async def get_writer(headers, params) -> dict:
    data = await _search(params, headers)
    writers_names = data and data[0].get('writers_names')
    if writers_names is None:
        return {'text_to_speech': messages.NOT_FOUND}
    return {
        'text_to_speech': f'Сценарист фильма {", ".join(writers_names)}',
        'persons': data[0]['writers'],
    }


async def get_duration(headers, params) -> dict:
    data = await _search(params, headers)
    duration = data and data[0].get('duration')
    if data is None:
        return {'text_to_speech': messages.NOT_FOUND}
    return {'text_to_speech': f'Длительность фильма {duration} минут'}


async def get_film_by_person(headers, params) -> dict:
    data = await _search(params, headers)
    if data is None:
        return {'text_to_speech': messages.NOT_FOUND}

    titles = ', '.join(film_data['title'] for film_data in data)
    return {
        'text_to_speech': f'Всего фильмов {len(data)}. Это - {titles}',
        'films': data,
    }
