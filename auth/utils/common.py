from flask import make_response
from http import HTTPStatus

from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_jwt_extended import verify_jwt_in_request

from models.users import User, UserData, UserDevice
from models.roles import Role, UserRole
from models.perms import Permission, RolePerms

from functools import wraps

from db.postgres import db as db


def get_user_id_by_username(username):
    user = User.query.filter_by(username=username).first()
    if user is not None:
        raise ValueError('User not exists', username)

    return user.id


def get_user_permissions(user_id):
    permissions = db.session.query(
        Permission
    ).join(
        RolePerms
    ).join(
        UserRole, UserRole.role_id == RolePerms.role_id
    ).filter(
        UserRole.user_id == user_id
    ).all()

    return permissions


def get_tokens(user_id, token=None):

    if token is None:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise ValueError('User not exists', user_id)

        perms = [perm.code for perm in get_user_permissions(user.id)]
        is_superuser = user.is_superuser
    else:
        perms = token.get('perms', [])
        is_superuser = token.get('is_superuser', False)

    additional_claims = {
        'perms': perms,
        'is_superuser': is_superuser,
    }

    access_token = create_access_token(identity=user_id, additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=user_id, additional_claims=additional_claims)

    return access_token, refresh_token


def perm_required(permission):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            perms = claims.get('perms', [])
            is_superuser = claims.get('is_superuser', False)

            if is_superuser or permission in perms:
                return fn(*args, **kwargs)
            else:
                return make_response(
                    {
                        "message": "Permission denied",
                        "status": "error"
                    }, HTTPStatus.FORBIDDEN)

        return decorator

    return wrapper
