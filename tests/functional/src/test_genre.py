import pytest

from ..testdata.genre import genre_by_id_expected, genre_list, genre_list_expected


@pytest.mark.asyncio
async def test_get_genre_by_id(send_data_to_elastic, genre_list, make_get_request, genre_by_id_expected):
    async with send_data_to_elastic(data=genre_list):
        response = await make_get_request('/genre/32345678-1234-1234-1234-123456789101')

        assert response.status == 200, 'genre doesn\'t available by id'
        assert len(response.body) == len(genre_by_id_expected), 'check fields count'
        assert response.body == genre_by_id_expected, 'check data in document'


@pytest.mark.asyncio
async def test_get_nonexistent_genre(send_data_to_elastic, genre_list, make_get_request):
    async with send_data_to_elastic(data=genre_list):
        response = await make_get_request('/genre/32345678-1234-1234-1234-123456789100')

        assert response.status == 404, 'available nonexistent genre'


@pytest.mark.asyncio
async def test_get_cached_genre(
    send_data_to_elastic, genre_list, make_get_request, genre_by_id_expected, clear_cache, es_client
):
    # testing scenario:
    # Send data to elastic, make GET request to api, delete data from elastic.
    # Confirm response, make another GET request to api. If cache available the second response would be successful.
    # Clear cache and repeat GET request to api. This time 404 error should be expected.
    async with send_data_to_elastic(data=genre_list, with_clear_cache=False):
        response = await make_get_request('/genre/32345678-1234-1234-1234-123456789101')
        assert response.body == genre_by_id_expected, 'check data in document'

    es_response = await es_client.get(index='genres', id='32345678-1234-1234-1234-123456789101', ignore=404)
    assert es_response.get('found') is False, 'data in elastic still exists after deletion'
    response = await make_get_request('/genre/32345678-1234-1234-1234-123456789101')
    assert response.status == 200, 'cache should be available'
    assert response.body == genre_by_id_expected, 'incorrect document in cache'

    await clear_cache()
    response = await make_get_request('/genre/32345678-1234-1234-1234-123456789101')
    assert response.status == 404, 'data in cache still exists after deletion'


@pytest.mark.asyncio
async def test_full_genre_list(send_data_to_elastic, genre_list, make_get_request, genre_list_expected):
    async with send_data_to_elastic(data=genre_list):
        response = await make_get_request('/genre')

        assert response.status == 200, 'genre list should be available'
        assert len(response.body) == len(genre_list_expected), 'check genre count'
        key_sort = lambda genre_info: genre_info['uuid']
        assert sorted(response.body, key=key_sort) == sorted(genre_list_expected, key=key_sort), \
            'check data in documents'


@pytest.mark.asyncio
async def test_genre_pagination(send_data_to_elastic, genre_list, make_get_request, genre_list_expected):
    # testing scenario:
    # we select page size that there are n-1 record on first page and 1 record on second page
    # check that page is available param

    async with send_data_to_elastic(data=genre_list):
        page_size = min(len(genre_list_expected) - 1, 29)
        response = await make_get_request(f'/genre?page[size]={page_size}&page[number]=1')

        assert response.status == 200, 'pagination should be available'
        assert len(response.body) == page_size, 'check genre count'

        page_size = len(genre_list_expected) - 1
        response = await make_get_request(f'/genre?page[size]={page_size}&page[number]=2')

        assert len(response.body) == 1, 'check genre count'

        response = await make_get_request('/genre?page[size]=-1')
        assert response.status == 400

        response = await make_get_request('/genre?page[size]=a')
        assert response.status == 400


@pytest.mark.asyncio
async def test_genre_text_search(send_data_to_elastic, genre_list, make_get_request):
    async with send_data_to_elastic(data=genre_list):
        response = await make_get_request('/genre/search?query=show')

        assert response.status == 200, 'text search should be available'
        assert len(response.body) == 2, 'search by name doesn\'t available'

        response = await make_get_request('/genre/search?query=science')

        assert len(response.body) == 2, 'search by description doesn\'t available'
