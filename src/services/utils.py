from typing import Any, Optional

from fastapi import Request
from pydantic.types import PositiveInt

from models.base import BaseModel


class Page(BaseModel):
    size: PositiveInt = 50
    number: PositiveInt = 1


class Filter(BaseModel):
    field: str
    value: str


class Body(BaseModel):
    query: Optional[str]
    sort: Optional[str]
    filter: Optional[Filter]
    page: Optional[Page]


def _validate_query_params(query: str = None, sort: str = None, page: dict = None, filter: dict = None) -> Body:
    """
    Args:
        sort: sorting field from url. If starts with '-' then desc order will be applied
        page[size]: number of hits on page
        page[number]: page number
        query: searching query, default 'match_all'
        filter: dict of filtered field and it's value
    """
    page = page and Page(**page)
    if filter is not None:
        field, value = tuple(filter.items())[0]
        filter = Filter(field=field, value=value)
    body = Body(query=query, sort=sort, filter=filter, page=page)
    return body


def get_body(**raw_params) -> dict[str, Any]:
    """Returns body for search query based on params given.

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
    query_body: dict[str, Any] = {}
    params = _validate_query_params(**raw_params)

    # pagination
    if params.page is not None:
        query_body['from'] = (params.page.number - 1) * params.page.size
        query_body['size'] = params.page.size

    # searching
    if params.query is not None:
        query_body.setdefault('query', {}).update(_get_search_query(params.query))
    elif params.filter is not None:
        query_body.setdefault('query', {}).update(_get_filter_query(params.filter))
    else:
        query_body['query'] = {'match_all': {}}

    # sorting
    if params.sort is not None:
        field = params.sort.removeprefix('-')
        direction = 'desc' if params.sort.startswith('-') else 'asc'
        query_body['sort'] = {
            field: {'order': direction}
        }

    return query_body


def _get_search_query(query: str) -> dict:
    return {
        # "simple_query_string": {
        "query_string": {
            "query": query
        }
    }


def _get_filter_query(filter: Filter) -> dict:
    # selected category is filtered based on id:UUID only
    nested_field = f'{filter.field}.id'
    return {
        "nested": {
            "path": filter.field,
            "query": {
                "bool": {
                    "must": [
                        {"match": {nested_field: filter.value}}
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
            params.setdefault(nested_key[0], {}).update({nested_key[1]: value})  # type: ignore
            continue
        params[key] = value

    return params
