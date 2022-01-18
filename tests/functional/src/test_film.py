import pytest

from ..testdata.film import film_by_id_expected, film_list


@pytest.mark.asyncio
async def test_get_film_by_id(send_data_to_elastic, film_list, make_get_request, film_by_id_expected):
    async with send_data_to_elastic(data=film_list):
        
        response = await make_get_request('/film/12345678-1234-1234-1234-123456789101')
    
        assert response.status == 200
        assert len(response.body) == 8
        assert response.body == film_by_id_expected
