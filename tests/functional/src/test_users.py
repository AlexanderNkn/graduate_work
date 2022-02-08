import pytest
from http import HTTPStatus

import json

from models.users import User, UserData

# создать нового пользователя (залогиниться), проверить наличие данных в базе psql
# создать пользователя, добавить ему перс.данные, проверить наличие перс.данных в базе
# создать пользователя, добавить ему перс.данные, изменить перс.данные, проверить изменение перс.данных в базе
# создать пользователя, залогиниться под ним, проверить успешность и наличие 2 токенов: access и refresh
# залогиниться под не существующим пользователем, получить ошибку 401
# залогиниться под пользователем, разлогиниться, выполнить доступ к ресурсам с его access токеном
# установить время access токена 1с, залогиниться, подождать 1с, доступ с токеном, должна быть ошибка
# установить время access и refresh токенов 1с, залогиниться, подождать 1с, попытаться получить refresh токен, должна быть ошибка


@pytest.fixture
def create_user(session):

    created_records = []

    def _create_user(username, password):
        user = User(username=username, password=password, is_superuser=True)
        created_records.append(username)
        session.add(user)
        session.commit()
        return user

    yield _create_user

    for username in created_records:
        User.query.filter_by(username=username).delete()
    session.commit()


@pytest.fixture
def login_user(client, create_user):
    # create user
    # login
    # return tokens

    def _login_user(username, password):
        user = create_user(username, password)
        body = json.dumps({'username': username, 'password': password})
        response = client.post(
            '/api/v1/auth/login',
            data=body,
            content_type='application/json',
        )

        if response.status_code == HTTPStatus.OK:
            return user, response.json['tokens']
        else:
            raise Exception('Bad login request')

    return _login_user


def test_register_user(client, session):
    body = json.dumps({'username': 'user1', 'password': '234'})
    response = client.post(
        '/api/v1/auth/register',
        data=body,
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.OK


def test_register_existent_user(client, session, create_user):
    user = create_user('user1', '234')
    body = json.dumps({'username': 'user1', 'password': '234'})
    response = client.post(
        '/api/v1/auth/register',
        data=body,
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_register_empty_username(client, session):
    body = json.dumps({'username': '', 'password': '234'})
    response = client.post(
        '/api/v1/auth/login',
        data=body,
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_register_without_username(client, session):
    body = json.dumps({'password': '234'})
    response = client.post(
        '/api/v1/auth/login',
        data=body,
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_login_user(client, session, create_user):
    user = create_user('user1', '234')
    body = json.dumps({'username': 'user1', 'password': '234'})
    response = client.post(
        '/api/v1/auth/login',
        data=body,
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.OK


def test_login_non_existent_user(client, session):
    body = json.dumps({'username': 'user2', 'password': '234'})
    response = client.post(
        '/api/v1/auth/login',
        data=body,
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_login_empty_user(client, session):
    body = json.dumps({'password': '234'})
    response = client.post(
        '/api/v1/auth/login',
        data=body,
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_login_empty_password(client, session):
    body = json.dumps({'user': 'user1'})
    response = client.post(
        '/api/v1/auth/login',
        data=body,
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_login_wrong_password(client, session, create_user):
    user = create_user('user1', '234')
    body = json.dumps({'username': 'user1', 'password': '345'})
    response = client.post(
        '/api/v1/auth/login',
        data=body,
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_logout(client, session, login_user):
    _, tokens = login_user('user1', '234')
    body = json.dumps({})
    response = client.post(
        '/api/v1/auth/logout',
        data=body,
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.OK


def test_refresh_token(client, session, login_user):
    _, tokens = login_user('user1', '234')
    refresh_token = tokens['refresh_token']
    body = json.dumps({'username': 'user1', 'password': '234'})
    response = client.post(
        '/api/v1/auth/refresh_token',
        data=body,
        content_type='application/json',
        headers={'Authorization': f'Bearer {refresh_token}'}
    )

    assert response.status_code == HTTPStatus.OK


def test_refresh_token_incorrect(client, session, login_user):
    _, tokens = login_user('user1', '234')
    refresh_token = tokens['refresh_token'] + '345345'
    body = json.dumps({'username': 'user1', 'password': '234'})
    response = client.post(
        '/api/v1/auth/refresh_token',
        data=body,
        content_type='application/json',
        headers={'Authorization': f'Bearer {refresh_token}'}
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_change_password(client, session, login_user):
    user, tokens = login_user('user1', '234')
    access_token = tokens['access_token']
    body = json.dumps({'old_password': '234', 'new_password': '345'})
    response = client.patch(
        f'/api/v1/auth/change_password/{user.id}',
        data=body,
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == HTTPStatus.OK


def test_change_password_wrong_password(client, session, login_user):
    user, tokens = login_user('user1', '234')
    access_token = tokens['access_token']
    body = json.dumps({'old_password': '345', 'new_password': '456'})
    response = client.patch(
        f'/api/v1/auth/change_password/{user.id}',
        data=body,
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_change_password_nonexistent_user(client, session, login_user):
    user, tokens = login_user('user1', '234')
    access_token = tokens['access_token']
    body = json.dumps({'old_password': '345', 'new_password': '456'})
    response = client.patch(
        f'/api/v1/auth/change_password/789',
        data=body,
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND

