import uuid
from functools import wraps
from http import HTTPStatus

from flask import make_response
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request


def permission_required(permission):
    """
    Проверяем наличие у пользователя права на доступ к ресурсу. Это возможно в одном из случаев:
     - это суперпользователь
     - у пользователя есть необходимый permission
     - пользователь работает со своими данными

    :param permission:
    :return:
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            uri_user_id = kwargs.get('user_id')

            if has_permission(uri_user_id, permission):
                return fn(*args, **kwargs)
            else:
                return make_response(
                    {
                        "message": "Permission denied",
                        "status": "error"
                    }, HTTPStatus.FORBIDDEN)

        return decorator

    return wrapper


def has_permission(user_id, permission):
    verify_jwt_in_request()

    token_user_id = uuid.UUID(get_jwt_identity())
    is_owner = user_id == token_user_id

    claims = get_jwt()
    permissions = claims.get('permissions', [])
    is_superuser = claims.get('is_superuser', False)

    return is_superuser or is_owner or permission in permissions
