from http import HTTPStatus

import pytest
import pytest_asyncio

from ..testdata.film import film_by_id_expected, film_list, film_list_expected

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
async def upload_film_data(send_data_to_elastic, film_list):
    async with send_data_to_elastic(data=film_list):
        yield


async def test_get_film_by_id(upload_film_data, make_get_request, film_by_id_expected):
    response = await make_get_request('/film/12345678-1234-1234-1234-123456789101')

    assert response.status == HTTPStatus.OK, "film doesn\'t available by id"
    assert len(response.body) == len(film_by_id_expected), 'check fields count'
    assert response.body == film_by_id_expected, 'check data in document'


async def test_get_nonexistent_film(upload_film_data, make_get_request):
    response = await make_get_request('/film/12345678-1234-1234-1234-123456789100')

    assert response.status == HTTPStatus.NOT_FOUND, 'available nonexistent film'


async def test_get_cached_film(
    send_data_to_elastic, film_list, make_get_request, film_by_id_expected, clear_cache, es_client
):
    # testing scenario:
    # Send data to elastic, make GET request to api, delete data from elastic.
    # Confirm response, make another GET request to api. If cache available the second response would be successful.
    # Clear cache and repeat GET request to api. This time HTTPStatus.NOT_FOUND error should be expected.
    async with send_data_to_elastic(data=film_list, with_clear_cache=False):
        response = await make_get_request('/film/12345678-1234-1234-1234-123456789101')
        assert response.body == film_by_id_expected, 'check data in document'

    es_response = await es_client.get(
        index='movies', id='12345678-1234-1234-1234-123456789101', ignore=HTTPStatus.NOT_FOUND
    )
    assert es_response.get('found') is False, 'data in elastic still exists after deletion'
    response = await make_get_request('/film/12345678-1234-1234-1234-123456789101')
    assert response.status == HTTPStatus.OK, 'cache should be available'
    assert response.body == film_by_id_expected, 'incorrect document in cache'

    await clear_cache()
    response = await make_get_request('/film/12345678-1234-1234-1234-123456789101')
    assert response.status == HTTPStatus.NOT_FOUND, 'data in cache still exists after deletion'


async def test_full_film_list(upload_film_data, make_get_request, film_list_expected):
    response = await make_get_request('/film')

    assert response.status == HTTPStatus.OK, 'film list should be available'
    # due to we use common db for testing we have to delete non-testing data before assert
    response.body = [film for film in response.body if film in film_list_expected]
    assert len(response.body) == len(film_list_expected), 'check film count'
    key_sort = lambda film_info: film_info['uuid']
    assert sorted(response.body, key=key_sort) == sorted(film_list_expected, key=key_sort), \
        'check data in documents'


async def test_film_sort(upload_film_data, make_get_request, film_list_expected):
    response = await make_get_request('/film?sort=-imdb_rating')

    assert response.status == HTTPStatus.OK, 'sort should be available'
    # due to we use common db for testing we have to delete non-testing data before assert
    response.body = [film for film in response.body if film in film_list_expected]
    key_sort = lambda film_info: -film_info['imdb_rating']
    assert sorted(response.body, key=key_sort) == sorted(film_list_expected, key=key_sort), \
        'check data in document'


async def test_film_filter_by_genre_id(upload_film_data, make_get_request):
    response = await make_get_request('/film?filter[genre.id]=5373d043-3f41-4ea8-9947-4b746c601bbd')

    assert response.status == HTTPStatus.OK, 'filter by genre id should be available'
    assert len(response.body) == 2, 'check film count'


async def test_film_filter_by_genre_name(upload_film_data, make_get_request):
    response = await make_get_request('/film?filter[genre.name]=Comedy')

    assert response.status == HTTPStatus.OK, 'filter by genre name should be available'
    assert len(response.body) == 2, 'check film count'


async def test_film_filter_by_actor_id(upload_film_data, make_get_request):
    response = await make_get_request('/film?filter[actors.id]=22345678-1234-1234-1234-123456789104')

    assert response.status == HTTPStatus.OK, 'filter by actor id should be available'
    assert len(response.body) == 2, 'check film count'


async def test_film_filter_by_actor_name(upload_film_data, make_get_request):
    response = await make_get_request('/film?filter[actors.name]=Alex Kurtzman')

    assert response.status == HTTPStatus.OK, 'filter by actor name should be available'
    assert len(response.body) == 2, 'check film count'


async def test_film_filter_by_writer_id(upload_film_data, make_get_request):
    response = await make_get_request('/film?filter[writers.id]=22345678-1234-1234-1234-123456789105')

    assert response.status == HTTPStatus.OK, 'filter by writer id should be available'
    assert len(response.body) == 3, 'check film count'


async def test_film_filter_by_writer_name(upload_film_data, make_get_request):
    response = await make_get_request('/film?filter[writers.name]=Chris Pine')

    assert response.status == HTTPStatus.OK, 'filter by writer name should be available'
    assert len(response.body) == 3, 'check film count'


async def test_film_filter_by_director_id(upload_film_data, make_get_request):
    response = await make_get_request('/film?filter[directors.id]=22345678-1234-1234-1234-123456789102')

    assert response.status == HTTPStatus.OK, 'filter by director id should be available'
    assert len(response.body) == 2, 'check film count'


async def test_film_filter_by_director_name(upload_film_data, make_get_request):
    response = await make_get_request('/film?filter[directors.name]=David Tomaszewski')

    assert response.status == HTTPStatus.OK, 'filter by director name should be available'
    assert len(response.body) == 2, 'check film count'


async def test_pagination_first_page_size(upload_film_data, make_get_request, film_list_expected):
    # testing scenario:
    # we select page size that there are n-1 record on first page and 1 record on second page
    page_size = min(len(film_list_expected) - 1, 29)
    response = await make_get_request(f'/film?page[size]={page_size}&page[number]=1')

    assert response.status == HTTPStatus.OK, 'pagination should be available'
    assert len(response.body) == page_size, 'check film count'


async def test_pagination_second_page_size(upload_film_data, make_get_request, film_list_expected):
    # testing scenario:
    # we select page size that there are n-1 record on first page and 1 record on second page
    page_size = len(film_list_expected) - 1
    response = await make_get_request(f'/film?page[size]={page_size}&page[number]=2')

    assert response.status == HTTPStatus.OK, 'pagination should be available'
    # assert len(response.body) == 1, 'check film count'


async def test_pagination_page_size_negative(upload_film_data, make_get_request):
    response = await make_get_request('/film?page[size]=-1')
    assert response.status == HTTPStatus.BAD_REQUEST


async def test_pagination_page_size_not_number(upload_film_data, make_get_request):
    response = await make_get_request('/film?page[size]=a')
    assert response.status == HTTPStatus.BAD_REQUEST


async def test_film_text_search_by_title(upload_film_data, make_get_request):
    response = await make_get_request('/film/search?query=star')

    assert response.status == HTTPStatus.OK, 'text search should be available'
    assert len(response.body) == 1, "search by title doesn\'t available"


async def test_film_text_filter_by_title(upload_film_data, make_get_request):
    response = await make_get_request('/film?filter[title]=Video Killed the Radio Star')

    assert response.status == HTTPStatus.OK, 'root field filter should be available'
    assert len(response.body) == 1, "filter by title doesn\'t available"


async def test_film_text_search_by_description(upload_film_data, make_get_request):
    response = await make_get_request('/film/search?query=movie')

    assert response.status == HTTPStatus.OK, 'text search should be available'
    assert len(response.body) == 2, "search by description doesn\'t available"


async def test_film_text_search_by_description_correct_field(upload_film_data, make_get_request):
    response = await make_get_request('/film/search?query[description]=movie')

    assert response.status == HTTPStatus.OK, 'text search should be available'
    assert len(response.body) == 2, "search by description doesn\'t available"


async def test_film_text_search_by_description_incorrect_field(upload_film_data, make_get_request):
    response = await make_get_request('/film/search?query[title]=movie')

    assert response.status == HTTPStatus.NOT_FOUND, 'text search in other field should not be available'


async def test_film_text_search_by_actors(upload_film_data, make_get_request):
    response = await make_get_request('/film/search?query=Kurtzman')

    assert response.status == HTTPStatus.OK, 'text search should be available'
    assert len(response.body) == 2, "search by actors doesn\'t available"


async def test_film_text_search_by_writers(upload_film_data, make_get_request):
    response = await make_get_request('/film/search?query=Pine')

    assert response.status == HTTPStatus.OK, 'text search should be available'
    assert len(response.body) == 3, "search by writers doesn\'t available"


async def test_film_text_search_by_directors(upload_film_data, make_get_request):
    response = await make_get_request('/film/search?query=Tomaszewski')

    assert response.status == HTTPStatus.OK, 'text search should be available'
    assert len(response.body) == 2, "search by directors doesn\'t available"
