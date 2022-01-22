import pytest

from ..testdata.film import film_by_id_expected, film_list, film_list_expected


@pytest.mark.asyncio
async def test_get_film_by_id(send_data_to_elastic, film_list, make_get_request, film_by_id_expected):
    async with send_data_to_elastic(data=film_list):
        response = await make_get_request('/film/12345678-1234-1234-1234-123456789101')

        assert response.status == 200, 'film doesn\'t available by id'
        assert len(response.body) == 8, 'check fields count'
        assert response.body == film_by_id_expected, 'check data in document'


@pytest.mark.asyncio
async def test_get_nonexistent_film(send_data_to_elastic, film_list, make_get_request, film_by_id_expected):
    async with send_data_to_elastic(data=film_list):
        response = await make_get_request('/film/12345678-1234-1234-1234-123456789100')

        assert response.status == 404, 'available nonexistent film'


@pytest.mark.asyncio
async def test_get_cached_film(
    send_data_to_elastic, film_list, make_get_request, film_by_id_expected, clear_cache, es_client
):
    # testing scenario:
    # Send data to elastic, make GET request to api, delete data from elastic.
    # Confirm response, make another GET request to api. If cache available the second response would be successful.
    # Clear cache and repeat GET request to api. This time 404 error should be expected.
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
async def test_full_film_list(send_data_to_elastic, film_list, make_get_request, film_list_expected):
    async with send_data_to_elastic(data=film_list):
        response = await make_get_request('/film')

        assert response.status == 200, 'film list should be available'
        assert len(response.body) == len(film_list_expected), 'check film count'
        key_sort = lambda film_info: film_info['uuid']
        assert sorted(response.body, key=key_sort) == sorted(film_list_expected, key=key_sort), 'check data in document'


@pytest.mark.asyncio
async def test_film_sort(send_data_to_elastic, film_list, make_get_request, film_list_expected):
    async with send_data_to_elastic(data=film_list):
        response = await make_get_request('/film?sort=-imdb_rating')

        assert response.status == 200, 'sort should be available'
        key_sort = lambda film_info: -film_info['imdb_rating']
        assert sorted(response.body, key=key_sort) == sorted(film_list_expected, key=key_sort), 'check data in document'


@pytest.mark.asyncio
async def test_film_filter(send_data_to_elastic, film_list, make_get_request, film_list_expected):
    # testing scenario:
    # check filter by: genre id, actor id, writer id, director id

    async with send_data_to_elastic(data=film_list):
        response = await make_get_request('/film?filter[genre]=5373d043-3f41-4ea8-9947-4b746c601bbd')

        assert response.status == 200, 'filter by genre should be available'
        assert len(response.body) == 2, 'check film count'

        response = await make_get_request('/film?filter[actors]=82b7dffe-6254-4598-b6ef-5be747193946')

        assert response.status == 200, 'filter by actor should be available'
        assert len(response.body) == 2, 'check film count'

        response = await make_get_request('/film?filter[writers]=9f38323f-5912-40d2-a90c-b56899746f2a')

        assert response.status == 200, 'filter by writer should be available'
        assert len(response.body) == 3, 'check film count'

        response = await make_get_request('/film?filter[directors]=41ac0f45-d12d-434a-81b4-3bb9c1ebd4e4')

        assert response.status == 200, 'filter by director should be available'
        assert len(response.body) == 2, 'check film count'


@pytest.mark.asyncio
async def test_film_pagination(send_data_to_elastic, film_list, make_get_request, film_list_expected):
    # testing scenario:
    # we select page size that there are n-1 record on first page and 1 record on second page
    # check that page is available param

    async with send_data_to_elastic(data=film_list):
        page_size = min(len(film_list_expected) - 1, 29)
        response = await make_get_request(f'/film?page[size]={page_size}&page[number]=1')

        assert response.status == 200, 'pagination should be available'
        assert len(response.body) == page_size, 'check film count'

        page_size = len(film_list_expected) - 1
        response = await make_get_request(f'/film?page[size]={page_size}&page[number]=2')

        assert len(response.body) == 1, 'check film count'

        response = await make_get_request(f'/film?page[size]=-1')
        assert response.status == 400

        response = await make_get_request(f'/film?page[size]=a')
        assert response.status == 400


@pytest.mark.asyncio
async def test_film_text_search(send_data_to_elastic, film_list, make_get_request, film_list_expected):
    # testing scenario:
    # check filter by: genre id, actor id, writer id, director id

    async with send_data_to_elastic(data=film_list):
        response = await make_get_request('/film/search?query=star')

        assert response.status == 200, 'text search should be available'
        assert len(response.body) == 1, 'search by title doesn\'t available'

        response = await make_get_request('/film/search?query=movie')

        assert len(response.body) == 2, 'search by description doesn\'t available'

        response = await make_get_request('/film/search?query=robert')

        assert len(response.body) == 1, 'search by actors doesn\'t available'
