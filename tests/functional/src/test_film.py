import pytest

from ..testdata.film import film_by_id_expected, film_list, film_list_expected


@pytest.mark.asyncio
async def test_get_film_by_id(send_data_to_elastic, film_list, make_get_request, film_by_id_expected, clear_cache):
    async with send_data_to_elastic(data=film_list):
        response = await make_get_request('/film/12345678-1234-1234-1234-123456789101')

        assert response.status == 200
        assert len(response.body) == 8, 'check fields count'
        assert response.body == film_by_id_expected, 'check data in document'


@pytest.mark.asyncio
async def test_full_film_list(send_data_to_elastic, film_list, make_get_request, film_list_expected, clear_cache):
    async with send_data_to_elastic(data=film_list):
        response = await make_get_request('/film')

        assert response.status == 200
        assert len(response.body) == 1, 'check fields count'
        assert response.body == film_list_expected, 'check data in document'


@pytest.mark.asyncio
async def test_get_cached_film(
    send_data_to_elastic, film_list, make_get_request, film_by_id_expected, clear_cache, es_client
):
    # testing scenario:
    # Send data to elastic, make GET request to api, delete data from elastic.
    # Confirm response, make another GET request to api. If cache available the second response would be successful.
    # Cleare cache and repeat GET request to api. This time 404 error should be expected.
    async with send_data_to_elastic(data=film_list, with_clear_cache=False):
        response = await make_get_request('/film/12345678-1234-1234-1234-123456789101')
        assert response.body == film_by_id_expected, 'check data in document'

    es_response = await es_client.get(index='movies', id='12345678-1234-1234-1234-123456789101', ignore=404)
    assert es_response.get('found') is False, 'data in elastic still exists after deletion'
    response = await make_get_request('/film/12345678-1234-1234-1234-123456789101')
    assert response.status == 200, 'cache should be available'
    assert response.body == film_by_id_expected, 'incorrect document in cache'

    await clear_cache()
    response = await make_get_request('/film/12345678-1234-1234-1234-123456789101')
    assert response.status == 404, 'data in cache still exists after deletion'


@pytest.mark.asyncio
async def test_get_nonexistent_film(
    send_data_to_elastic, film_list, make_get_request, film_by_id_expected, clear_cache, es_client
):
    async with send_data_to_elastic(data=film_list):
        response = await make_get_request('/film/12345678-1234-1234-1234-123456789100')

        assert response.status == 404
