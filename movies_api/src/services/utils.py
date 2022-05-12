from typing import Any

from fastapi import Request
from fastapi.exceptions import HTTPException
from pydantic import ValidationError
from pydantic.types import PositiveInt

from models.base import BaseModel


class Page(BaseModel):
    size: PositiveInt = 50
    number: PositiveInt = 1


class Filter(BaseModel):
    field: str
    value: str


class Should(BaseModel):
    field: str
    value: str


class Body(BaseModel):
    query: str | dict[str, str] | None
    sort: str | None
    filter: Filter | None
    should: list[Should] | None
    page: Page | None


def _validate_query_params(
    query: str = None,
    sort: str = None,
    page: dict = None,
    filter: dict = None,
    should: list = None,
    all: bool = None,
) -> Body:
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
    if should is not None:
        should_list = []
        for should_item in should:
            field, value = tuple(should_item.items())[0]
            should_list.append(Should(field=field, value=value))
        should = should_list
    return Body(query=query, sort=sort, filter=filter, page=page, should=should)


def get_body(**raw_params) -> dict[str, Any]:
    """Returns body for search query based on params given.

    Returns:
        Example
        {
          'from': 5,
          'size': 20,
          'query': {
            'match_all': {}
          },
          'sort': {
            'field': {'order': 'desc'}
          },
          ...
        }
    """
    query_body: dict[str, Any] = {}
    try:
        params = _validate_query_params(**raw_params)
    except ValidationError:
        raise HTTPException(status_code=400, detail='Invalid query parameters')

    # pagination
    if params.page is not None:
        query_body['from'] = (params.page.number - 1) * params.page.size
        query_body['size'] = params.page.size

    # searching
    query_body['query'] = {'match_all': {}}
    filters = []
    if params.query is not None:
        filters.append(_get_search_query(params.query))
    if params.filter is not None:
        filters.append(_get_filter_query(params.filter))
    if params.should is not None:
        filters.append(_get_should_query(params.should))
    if filters:
        query_body['query'] = {
            'bool': {
                'must': filters
            }
        }

    # sorting
    if params.sort is not None:
        field = params.sort.removeprefix('-')
        direction = 'desc' if params.sort.startswith('-') else 'asc'
        query_body['sort'] = {
            field: {'order': direction}
        }

    return query_body


def _get_search_query(query: str | dict[str, str]) -> dict:
    """Prepares query depends on params.

    The search query can by run against specified fields otherwise all fields will be used.
    Example:
        /movies-api/v1/film/search?query[title,description]=Edge of tomorrow
        checks query string in title and description only.

        This phrase will be searched in all fields
        /movies-api/v1/film/search?query=Edge of tomorrow
    """
    fields = []
    if isinstance(query, dict):
        fields_string, query = next(iter(query.items()))
        fields = fields_string.split(',')
    return {
        'query_string': {
            'query': query,
            'fields': fields,
        }
    }


def _get_filter_query(filter: Filter) -> dict:
    """Prepares filters depends on Elastic index schema.

    Nested fields should be passed as filter params using dot notation.
    Example:
        schema:
            "actors_names": [
                "Emily Blunt",
                "Tom Cruise"
            ],
            "directors": [
                {
                    "id": "e155043e-c6aa-4135-87db-2b30e6208250",
                    "name": "Doug Liman"
                }
            ],
            ...
        related filter queries:
            /movies-api/v1/film/search?filter[actors_names]=Emily Blunt
            /movies-api/v1/film/search?filter[directors.id]=e155043e-c6aa-4135-87db-2b30e6208250
            /movies-api/v1/film/search?filter[directors.name]=Doug Liman
    """
    query = {
                'bool': {
                    'must': [
                        {'match': {filter.field: filter.value}}
                    ]
                }
            }
    if len(path := filter.field.split('.')[0]) == len(filter.field):
        return query

    return {
        'nested': {
            'path': path,
            'query': query
        }
    }


def _get_should_query(should_list: list[Should]) -> dict:
    # selected items by id in list
    return {
        'bool': {
            'should': [
                {'match': {should.field: should.value}} for should in should_list
            ]
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
