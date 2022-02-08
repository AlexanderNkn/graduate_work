import pytest
from http import HTTPStatus

import json

# создать нового пользователя (залогиниться), проверить наличие данных в базе psql
# создать пользователя, добавить ему перс.данные, проверить наличие перс.данных в базе
# создать пользователя, добавить ему перс.данные, изменить перс.данные, проверить изменение перс.данных в базе
# создать пользователя, залогиниться под ним, проверить успешность и наличие 2 токенов: access и refresh
# залогиниться под не существующим пользователем, получить ошибку 401
# залогиниться под пользователем, разлогиниться, выполнить доступ к ресурсам с его access токеном
# установить время access токена 1с, залогиниться, подождать 1с, доступ с токеном, должна быть ошибка
# установить время access и refresh токенов 1с, залогиниться, подождать 1с, попытаться получить refresh токен, должна быть ошибка


def test_register_user(app, db):
    body = json.dumps({'username': 'user1', 'password': '234'})
    response = app.test_client().post(
        '/api/v1/auth/register',
        data=body,
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.OK


def test_register_empty_user(app, db):
    body = json.dumps({'username': '', 'password': '234'})
    response = app.test_client().post(
        '/api/v1/auth/login',
        data=body,
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_register_without_username(app, db):
    body = json.dumps({'password': '234'})
    response = app.test_client().post(
        '/api/v1/auth/login',
        data=body,
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_login_user(app, db):
    body = json.dumps({'username': 'user1', 'password': '234'})
    response = app.test_client().post(
        '/api/v1/auth/login',
        data=body,
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_login_non_existent_user(app, db):
    body = json.dumps({'username': 'user2', 'password': '234'})
    response = app.test_client().post(
        '/api/v1/auth/login',
        data=body,
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_login_empty_user(app, db):
    body = json.dumps({'password': '234'})
    response = app.test_client().post(
        '/api/v1/auth/login',
        data=body,
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_login_empty_password(app, db):
    body = json.dumps({'user': 'user1'})
    response = app.test_client().post(
        '/api/v1/auth/login',
        data=body,
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


