from itsdangerous import json
import pytest
# import pytest_asyncio

from flask import Flask
from auth.api.v1 import auth, role

from .settings import settings


@pytest.fixture
def admin_token(client):
    response = client.post('/login', json={'username': 'username', 'password': 'password'}
    )
    access_token = response.tokens.access_token
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    return headers

@pytest.fixture
def user_token(client):
    response = client.post('/login', json={'username': 'username', 'password': 'password'}
    )
    access_token = response.tokens.access_token
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    return headers
