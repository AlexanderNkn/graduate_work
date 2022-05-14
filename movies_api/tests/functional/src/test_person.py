from http import HTTPStatus

import pytest
import pytest_asyncio

from ..testdata.film import film_list
from ..testdata.person import film_list_expected, person_by_id_expected, person_list, person_list_expected

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
async def upload_person_data(send_data_to_elastic, person_list):
    async with send_data_to_elastic(data=person_list):
        yield


async def test_get_person_by_id(upload_person_data, make_get_request, person_by_id_expected):
    response = await make_get_request('/person/22345678-1234-1234-1234-123456789101')

    assert response.status == HTTPStatus.OK, "person doesn\'t available by id"
    assert len(response.body) == len(person_by_id_expected), 'check fields count'
    assert response.body == person_by_id_expected, 'check data in document'


async def test_get_nonexistent_person(upload_person_data, make_get_request):
    response = await make_get_request('/person/22345678-1234-1234-1234-123456789100')
    assert response.status == HTTPStatus.NOT_FOUND, 'available nonexistent person'


async def test_get_cached_person(
    send_data_to_elastic, person_list, make_get_request, person_by_id_expected, clear_cache, es_client
):
    # testing scenario:
    # Send data to elastic, make GET request to api, delete data from elastic.
    # Confirm response, make another GET request to api. If cache available the second response would be successful.
    # Clear cache and repeat GET request to api. This time HTTPStatus.NOT_FOUND error should be expected.
    async with send_data_to_elastic(data=person_list, with_clear_cache=False):
        response = await make_get_request('/person/22345678-1234-1234-1234-123456789101')
        assert response.body == person_by_id_expected, 'check data in document'

    es_response = await es_client.get(
        index='persons', id='22345678-1234-1234-1234-123456789101', ignore=HTTPStatus.NOT_FOUND
    )
    assert es_response.get('found') is False, 'data in elastic still exists after deletion'
    response = await make_get_request('/person/22345678-1234-1234-1234-123456789101')
    assert response.status == HTTPStatus.OK, 'cache should be available'
    assert response.body == person_by_id_expected, 'incorrect document in cache'

    await clear_cache()
    response = await make_get_request('/person/22345678-1234-1234-1234-123456789101')
    assert response.status == HTTPStatus.NOT_FOUND, 'data in cache still exists after deletion'


async def test_full_person_list(upload_person_data, make_get_request, person_list_expected):
    response = await make_get_request('/person')

    assert response.status == HTTPStatus.OK, 'person list should be available'
    # due to we use common db for testing we have to delete non-testing data before assert
    response.body = [person for person in response.body if person in person_list_expected]
    assert len(response.body) == len(person_list_expected), 'check person count'
    key_sort = lambda person_info: person_info['uuid']
    assert sorted(response.body, key=key_sort) == sorted(person_list_expected, key=key_sort), \
        'check data in documents'


async def test_person_film_list(
    send_data_to_elastic, upload_person_data, film_list, make_get_request, film_list_expected
):
    async with send_data_to_elastic(data=film_list):
        response = await make_get_request('/person/22345678-1234-1234-1234-123456789102/film')

        assert response.status == HTTPStatus.OK, 'film list by person should be available'
        assert len(response.body) == len(film_list_expected), 'check film count'
        key_sort = lambda person_info: person_info['uuid']
        assert sorted(response.body, key=key_sort) == sorted(film_list_expected, key=key_sort), \
            'check data in documents'


async def test_pagination_first_page_size(upload_person_data, make_get_request, person_list_expected):
    # testing scenario:
    # we select page size that there are n-1 record on first page and 1 record on second page
    page_size = min(len(person_list_expected) - 1, 29)
    response = await make_get_request(f'/person?page[size]={page_size}&page[number]=1')

    assert response.status == HTTPStatus.OK, 'pagination should be available'
    assert len(response.body) == page_size, 'check person count'


async def test_pagination_second_page_size(upload_person_data, make_get_request, person_list_expected):
    # testing scenario:
    # we select page size that there are n-1 record on first page and 1 record on second page
    page_size = len(person_list_expected) - 1
    response = await make_get_request(f'/person?page[size]={page_size}&page[number]=2')

    assert response.status == HTTPStatus.OK, 'pagination should be available'
    # assert len(response.body) == 1, 'check person count'


async def test_pagination_page_size_negative(upload_person_data, make_get_request):
    response = await make_get_request('/person?page[size]=-1')
    assert response.status == HTTPStatus.BAD_REQUEST


async def test_pagination_page_size_not_number(upload_person_data, make_get_request):
    response = await make_get_request('/person?page[size]=a')
    assert response.status == HTTPStatus.BAD_REQUEST


async def test_person_text_search_by_name(upload_person_data, make_get_request):
    response = await make_get_request('/person/search?query=chris')

    assert response.status == HTTPStatus.OK, 'text search should be available'
    assert len(response.body) == 2, "search by name doesn\'t available"


async def test_person_text_search_by_role(upload_person_data, make_get_request, person_list_expected):
    response = await make_get_request('/person/search?query=actor')

    assert response.status == HTTPStatus.OK, 'text search should be available'
    # due to we use common db for testing we have to delete non-testing data before assert
    response.body = [person for person in response.body if person in person_list_expected]
    assert len(response.body) == 4, "search by role doesn\'t available"
