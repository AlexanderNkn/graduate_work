"""Module contains methods for fetching data from movies_api with further processing."""
from core import config

from .utils import make_get_request

# The common url for all requests to movies api
URL = f'{config.MOVIESAPI_HOST}:{config.MOVIESAPI_PORT}{config.MOVIESAPI_BASE_URL}'


def get_handler(intent: str):
    """Maps intent with its method."""
    return {
        'director_search': get_director,
        'actor_search': get_actor,
        'writer_search': get_writer,
        'film_by_person': get_film_by_person,
        # TODO add methods for other intents
    }.get(intent)


async def get_director(headers, params):
    fields = ','.join(params.keys())
    values = ' '.join(params.values())
    url = f'{URL}/film/search?query[{fields}]={values}&all=true'
    data = await make_get_request(url, headers)
    directors = ' '.join(data[0]['directors_names'])
    return {'text_to_speech': f'Режиссер фильма {directors}'}


async def get_actor(headers, params):
    fields = ','.join(params.keys())
    values = ' '.join(params.values())
    url = f'{URL}/film/search?query[{fields}]={values}&all=true'
    data = await make_get_request(url, headers)
    actors = ' '.join(data[0]['actors_names'])
    return {'text_to_speech': f'Актеры фильма {actors}'}


async def get_writer(headers, params):
    fields = ','.join(params.keys())
    values = ' '.join(params.values())
    url = f'{URL}/film/search?query[{fields}]={values}&all=true'
    data = await make_get_request(url, headers)
    writers = ' '.join(data[0]['writers_names'])
    return {'text_to_speech': f'Сценарист фильма {writers}'}


async def get_film_by_person(headers, params):
    fields = ','.join(params.keys())
    values = ' '.join(params.values())
    url = f'{URL}/film/search?query[{fields}]={values}'
    data = await make_get_request(url, headers)
    titles = ' '.join(film_data['title'] for film_data in data)
    return {'text_to_speech': f'Фильмы {titles}'}
