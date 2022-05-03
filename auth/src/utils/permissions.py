import uuid
from functools import wraps
from http import HTTPStatus

from flask import make_response
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request

from extensions import cache
from utils.jaeger import trace


def permission_required(permission):
    """
    Checks if user has access to specified endpoint. Any of these grant acces:
     - user is superuser
     - user has special permission
     - user is data owner

    :param permission:
    :return:
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()

            token_user_id = uuid.UUID(get_jwt_identity())
            uri_user_id = kwargs.get('user_id')
            if has_permission(user_id=uri_user_id, token_user_id=token_user_id, permission=permission):
                return fn(*args, **kwargs)
            else:
                return make_response(
                    {
                        "message": "Permission denied",
                        "status": "error"
                    }, HTTPStatus.FORBIDDEN)

        return decorator

    return wrapper


@trace
@cache.memoize(timeout=60)
def has_permission(permission: str, token_user_id: uuid.UUID, user_id: uuid.UUID | None = None) -> bool:
    is_owner = user_id == token_user_id

    claims = get_jwt()
    permissions = claims.get('permissions', [])
    is_superuser = claims.get('is_superuser', False)

    return is_superuser or is_owner or permission in permissions
