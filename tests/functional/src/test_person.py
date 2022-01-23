import pytest

from ..testdata.film import film_list
from ..testdata.person import film_list_expected, person_by_id_expected, person_list, person_list_expected


@pytest.mark.asyncio
async def test_get_person_by_id(send_data_to_elastic, person_list, make_get_request, person_by_id_expected):
    async with send_data_to_elastic(data=person_list):
        response = await make_get_request('/person/22345678-1234-1234-1234-123456789101')

        assert response.status == 200, 'person doesn\'t available by id'
        assert len(response.body) == len(person_by_id_expected), 'check fields count'
        assert response.body == person_by_id_expected, 'check data in document'


@pytest.mark.asyncio
async def test_get_nonexistent_person(send_data_to_elastic, person_list, make_get_request):
    async with send_data_to_elastic(data=person_list):
        response = await make_get_request('/person/22345678-1234-1234-1234-123456789100')

        assert response.status == 404, 'available nonexistent person'


@pytest.mark.asyncio
async def test_get_cached_person(
    send_data_to_elastic, person_list, make_get_request, person_by_id_expected, clear_cache, es_client
):
    # testing scenario:
    # Send data to elastic, make GET request to api, delete data from elastic.
    # Confirm response, make another GET request to api. If cache available the second response would be successful.
    # Clear cache and repeat GET request to api. This time 404 error should be expected.
    async with send_data_to_elastic(data=person_list, with_clear_cache=False):
        response = await make_get_request('/person/22345678-1234-1234-1234-123456789101')
        assert response.body == person_by_id_expected, 'check data in document'

    es_response = await es_client.get(index='persons', id='22345678-1234-1234-1234-123456789101', ignore=404)
    assert es_response.get('found') is False, 'data in elastic still exists after deletion'
    response = await make_get_request('/person/22345678-1234-1234-1234-123456789101')
    assert response.status == 200, 'cache should be available'
    assert response.body == person_by_id_expected, 'incorrect document in cache'

    await clear_cache()
    response = await make_get_request('/person/22345678-1234-1234-1234-123456789101')
    assert response.status == 404, 'data in cache still exists after deletion'


@pytest.mark.asyncio
async def test_full_person_list(send_data_to_elastic, person_list, make_get_request, person_list_expected):
    async with send_data_to_elastic(data=person_list):
        response = await make_get_request('/person')

        assert response.status == 200, 'person list should be available'
        assert len(response.body) == len(person_list_expected), 'check person count'
        key_sort = lambda person_info: person_info['uuid']
        assert sorted(response.body, key=key_sort) == sorted(person_list_expected, key=key_sort), \
            'check data in documents'


@pytest.mark.asyncio
async def test_person_film_list(send_data_to_elastic, person_list, film_list, make_get_request, film_list_expected):
    async with send_data_to_elastic(data=person_list):
        async with send_data_to_elastic(data=film_list):
            response = await make_get_request('/person/22345678-1234-1234-1234-123456789102/film')

            assert response.status == 200, 'film list by person should be available'
            assert len(response.body) == len(film_list_expected), 'check film count'
            key_sort = lambda person_info: person_info['uuid']
            assert sorted(response.body, key=key_sort) == sorted(film_list_expected, key=key_sort), \
                'check data in documents'


@pytest.mark.asyncio
async def test_person_pagination(send_data_to_elastic, person_list, make_get_request, person_list_expected):
    # testing scenario:
    # we select page size that there are n-1 record on first page and 1 record on second page
    # check that page is available param

    async with send_data_to_elastic(data=person_list):
        page_size = min(len(person_list_expected) - 1, 29)
        response = await make_get_request(f'/person?page[size]={page_size}&page[number]=1')

        assert response.status == 200, 'pagination should be available'
        assert len(response.body) == page_size, 'check person count'

        page_size = len(person_list_expected) - 1
        response = await make_get_request(f'/person?page[size]={page_size}&page[number]=2')

        assert len(response.body) == 1, 'check person count'

        response = await make_get_request('/person?page[size]=-1')
        assert response.status == 400

        response = await make_get_request('/person?page[size]=a')
        assert response.status == 400


@pytest.mark.asyncio
async def test_person_text_search(send_data_to_elastic, person_list, make_get_request):
    async with send_data_to_elastic(data=person_list):
        response = await make_get_request('/person/search?query=chris')

        assert response.status == 200, 'text search should be available'
        assert len(response.body) == 2, 'search by name doesn\'t available'

        response = await make_get_request('/person/search?query=actor')

        assert len(response.body) == 4, 'search by role doesn\'t available'
