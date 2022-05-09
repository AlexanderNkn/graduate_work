"""Module contains methods for fetching data from movies_api with further processing."""
from core import config

from .utils import make_get_request

# The common url for all requests to movies api
URL = f'{config.MOVIESAPI_HOST}:{config.MOVIESAPI_PORT}{config.MOVIESAPI_BASE_URL}'


def get_handler(intent: str):
    """Mapps intent with its method."""
    return {
        'director_search': get_director,
        # TODO add methods for other intents
    }.get(intent)


async def get_director(headers, params):
    fields = ','.join(params.keys())
    values = ' '.join(params.values())
    url = f'{URL}/film/search?query[{fields}]={values}&all=true'
    data = await make_get_request(url, headers)
    directors = ' '.join(data[0]['directors_names'])
    return f'Режиссер фильма {directors}'
