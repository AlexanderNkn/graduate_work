"""Module contains methods for fetching data from movies_api with further processing."""
from core import config, messages

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
    if isinstance(data, dict) and data.get('directors') is None:
        return {'text_to_speech': messages.NOT_FOUND}
    directors_names = ' '.join(data[0]['directors_names'])
    directors = data[0]['directors']
    return {
        'text_to_speech': f'Режиссер фильма {directors_names}',
        'persons': directors,
        }
