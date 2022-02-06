import pytest
from auth.main import app
from flask_jwt_extended import create_access_token


app.testing = True


@pytest.fixture(scope='session')
def admin_access_token():
    access_token = create_access_token('admin')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    return headers

@pytest.fixture(scope='session')
def user_access_token():
    access_token = create_access_token('subscriber')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    return headers

@pytest.fixture(scope='session')
def test_client():
    with app.test_client() as testing_client:
        yield testing_client
