from typing import Any

from fastapi import Request


def get_body(query: str = None, sort: str = None, page: dict = None, filter: dict = None) -> dict[str, Any]:
    """Returns body for search query based on args given.

    Args:
        sort: sorting field from url. If starts with '-' then desc order will be applied
        page[size]: number of hits on page
        page[number]: page number
        query: searching query, default 'match_all'
        filter: filtered field

    Returns:
        Example
        {
          "from": 5,
          "size": 20,
          "query": {
            "match_all": {}
          },
          "sort": {
            "field": {"order": "desc"}
          },
          ...
        }

    """
    # TODO add validation for query params
    body: dict[str, Any] = {}
    
    # pagination
    if page is not None:
        body['from'] = (int(page['number']) - 1) * int(page['size'])
        body['size'] = int(page['size'])
    
    # searching
    if query is not None:
        body.setdefault('query', {}).update(_get_search_query(query))
    elif filter is not None:
        body.setdefault('query', {}).update(_get_filter_query(filter))
    else:
        body['query'] = {'match_all': {}}
    
    # sorting
    if sort is not None:
        field = sort.removeprefix('-')
        direction = 'desc' if sort.startswith('-') else 'asc'
        body['sort'] = {
            field: {'order': direction}
        }

    return body


def _get_search_query(query: str) -> dict:
    # TODO
    pass


def _get_filter_query(filter: dict) -> dict:
    path, value = tuple(filter.items())[0]
    # selected category is filtered based on id:UUID only
    field = f'{path}.id'
    return {
        "nested": {
            "path": path,
            "query": {
                "bool": {
                    "must": [
                        {"match": {field: value}}
                    ]
                }
            }
        }
    }


def get_params(request: Request) -> dict[str, str | dict]:
    """Parses query params and collects them in dict.

    Example:
        from ?filter[genre]=<uuid>&sort=-imdb_rating&page[size]=50&page[number]=1 returns
        {
            'sort': '-imdb_rating',
            'page': {
                'size': '50',
                'number': '1'
            },
            'filter': {
              'genre': 'uuid'
            }
        }
    """
    params: dict[str, str | dict] = {}
    for key, value in request.query_params.items():
        nested_key = key.removesuffix(']').split('[')
        if len(nested_key) == 2:
            params.setdefault(nested_key[0], {}).update({nested_key[1]: value})  #type: ignore
            continue
        params[key] = value

    return params
