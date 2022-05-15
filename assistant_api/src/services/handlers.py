"""Module contains methods for fetching data from movies_api with further processing."""
from fastapi import HTTPException

from core import config, messages

from .utils import make_get_request

# The common url for all requests to movies api
URL = f'{config.MOVIESAPI_HOST}:{config.MOVIESAPI_PORT}{config.MOVIESAPI_BASE_URL}'


def get_handler(intent: str):
    """Maps intent with its method."""
    return {
        'director_search': get_director,
        'actor_search': get_actor,
        'writer_search': get_writer,
        'duration_search': get_duration,
        'film_by_person': get_film_by_person,
    }.get(intent)


async def _search(params, headers):
    fields = ','.join(params.keys())
    values = ' '.join(params.values())
    url = f'{URL}/film/search?query[{fields}]={values}&all=true'
    return await make_get_request(url, headers)


async def get_director(headers, params):
    data = await _search(params, headers)
    if not data:
        return {
            'text_to_speech': messages.NOT_FOUND
        }

    directors_names = data[0]['directors_names']
    if directors_names:
        directors = ' '.join(directors_names)
        persons = data[0]['directors']
        return {
            'text_to_speech': f'Режиссер фильма {directors}',
            'persons': persons,
        }
    return {
        'text_to_speech': messages.NOT_FOUND
    }


async def get_actor(headers, params):
    data = await _search(params, headers)
    if not data:
        return {
            'text_to_speech': messages.NOT_FOUND
        }

    actors_names = data[0]['actors_names']
    if actors_names:
        actors = ' '.join(actors_names)
        persons = data[0]['actors']
        return {
            'text_to_speech': f'Актеры фильма {actors}',
            'persons': persons,
        }
    return {
        'text_to_speech': messages.NOT_FOUND
    }


async def get_writer(headers, params):
    data = await _search(params, headers)
    if not data:
        return {
            'text_to_speech': messages.NOT_FOUND
        }

    writers_names = data[0]['writers_names']
    if writers_names:
        writers = ' '.join(writers_names)
        persons = data[0]['writers']
        return {
            'text_to_speech': f'Сценарист фильма {writers}',
            'persons': persons,
        }
    return {
        'text_to_speech': messages.NOT_FOUND
    }


async def get_duration(headers, params):
    data = await _search(params, headers)
    if not data:
        return {
            'text_to_speech': messages.NOT_FOUND
        }

    duration = data[0]['duration']
    if duration:
        return {
            'text_to_speech': f'Длительность фильма {duration} минут'
        }

    return {
        'text_to_speech': messages.NOT_FOUND
    }


async def get_film_by_person(headers, params):
    data = await _search(params, headers)
    if not data:
        return {
            'text_to_speech': messages.NOT_FOUND
        }

    titles = ' '.join(film_data['title'] for film_data in data)
    if titles:
        return {'text_to_speech': f'Фильмы {titles}'}

    return {
        'text_to_speech': messages.NOT_FOUND
    }
