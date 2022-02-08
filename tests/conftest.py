from itsdangerous import json
import pytest
# import pytest_asyncio

from flask import Flask
from auth.api.v1 import auth, role

from .settings import settings


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(auth.blueprint)
    app.register_blueprint(role.blueprint)

    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def create_admin_user(db):
    user = User(username='test_admin', pwd_hash=generate_password_hash('admin'), is_superuser=True)
    db.session.add(user)
    db.session.commit()

@pytest.fixture
def create_user(db):
    user = User(username='test_user', pwd_hash=generate_password_hash('user'))
    db.session.add(user)
    db.session.commit()

@pytest.fixture
def admin_token(client):
    response = client.post('/login', json={'username': 'test_admin', 'password': 'admin'}
    )
    access_token = response.tokens.access_token
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    return headers

@pytest.fixture
def user_token(client):
    response = client.post('/login', json={'username': 'test_user', 'password': 'user'}
    )
    access_token = response.tokens.access_token
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    return headers
