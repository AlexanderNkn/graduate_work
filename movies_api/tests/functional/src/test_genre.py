from http import HTTPStatus

import pytest
import pytest_asyncio

from ..testdata.genre import genre_by_id_expected, genre_list, genre_list_expected

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
async def upload_genre_data(send_data_to_elastic, genre_list):
    async with send_data_to_elastic(data=genre_list):
        yield


async def test_get_genre_by_id(upload_genre_data, make_get_request, genre_by_id_expected):
    response = await make_get_request('/genre/32345678-1234-1234-1234-123456789101')

    assert response.status == HTTPStatus.OK, "genre doesn\'t available by id"
    assert len(response.body) == len(genre_by_id_expected), 'check fields count'
    assert response.body == genre_by_id_expected, 'check data in document'


async def test_get_nonexistent_genre(upload_genre_data, make_get_request):
    response = await make_get_request('/genre/32345678-1234-1234-1234-123456789100')

    assert response.status == HTTPStatus.NOT_FOUND, 'available nonexistent genre'


async def test_get_cached_genre(
    send_data_to_elastic, genre_list, make_get_request, genre_by_id_expected, clear_cache, es_client
):
    # testing scenario:
    # Send data to elastic, make GET request to api, delete data from elastic.
    # Confirm response, make another GET request to api. If cache available the second response would be successful.
    # Clear cache and repeat GET request to api. This time HTTPStatus.NOT_FOUND error should be expected.
    async with send_data_to_elastic(data=genre_list, with_clear_cache=False):
        response = await make_get_request('/genre/32345678-1234-1234-1234-123456789101')
        assert response.body == genre_by_id_expected, 'check data in document'

    es_response = await es_client.get(
        index='genres', id='32345678-1234-1234-1234-123456789101', ignore=HTTPStatus.NOT_FOUND
    )
    assert es_response.get('found') is False, 'data in elastic still exists after deletion'
    response = await make_get_request('/genre/32345678-1234-1234-1234-123456789101')
    assert response.status == HTTPStatus.OK, 'cache should be available'
    assert response.body == genre_by_id_expected, 'incorrect document in cache'

    await clear_cache()
    response = await make_get_request('/genre/32345678-1234-1234-1234-123456789101')
    assert response.status == HTTPStatus.NOT_FOUND, 'data in cache still exists after deletion'


async def test_full_genre_list(upload_genre_data, make_get_request, genre_list_expected):
    response = await make_get_request('/genre')

    assert response.status == HTTPStatus.OK, 'genre list should be available'
    # due to we use common db for testing we have to delete non-testing data before assert
    response.body = [genre for genre in response.body if genre in genre_list_expected]
    assert len(response.body) == len(genre_list_expected), 'check genre count'
    key_sort = lambda genre_info: genre_info['uuid']
    assert sorted(response.body, key=key_sort) == sorted(genre_list_expected, key=key_sort), \
        'check data in documents'


async def test_pagination_first_page_size(upload_genre_data, make_get_request, genre_list_expected):
    # testing scenario:
    # we select page size that there are n-1 record on first page and 1 record on second page
    page_size = min(len(genre_list_expected) - 1, 29)
    response = await make_get_request(f'/genre?page[size]={page_size}&page[number]=1')

    assert response.status == HTTPStatus.OK, 'pagination should be available'
    assert len(response.body) == page_size, 'check genre count'


async def test_pagination_second_page_size(upload_genre_data, make_get_request, genre_list_expected):
    # testing scenario:
    # we select page size that there are n-1 record on first page and 1 record on second page
    page_size = len(genre_list_expected) - 1
    response = await make_get_request(f'/genre?page[size]={page_size}&page[number]=2')

    assert response.status == HTTPStatus.OK, 'pagination should be available'
    # assert len(response.body) == 1, 'check genre count'


async def test_pagination_page_size_negative(upload_genre_data, make_get_request):
    response = await make_get_request('/genre?page[size]=-1')
    assert response.status == HTTPStatus.BAD_REQUEST


async def test_pagination_page_size_not_number(upload_genre_data, make_get_request):
    response = await make_get_request('/genre?page[size]=a')
    assert response.status == HTTPStatus.BAD_REQUEST


async def test_genre_text_search_by_title(upload_genre_data, make_get_request):
    response = await make_get_request('/genre/search?query=show')

    assert response.status == HTTPStatus.OK, 'text search should be available'
    assert len(response.body) == 2, "search by name doesn\'t available"


async def test_genre_text_search_by_description(upload_genre_data, make_get_request):
    response = await make_get_request('/genre/search?query=science')

    assert response.status == HTTPStatus.OK, 'text search should be available'
    assert len(response.body) == 2, "search by description doesn\'t available"
