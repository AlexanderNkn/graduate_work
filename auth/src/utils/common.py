from http import HTTPStatus

from flask import make_response
from flask_jwt_extended import create_access_token, create_refresh_token

from extensions import db
from models import Permission, RolePermissions, User, UserRole
from utils.jaeger import trace


def check_empty_user_password(username, password):
    if not username or not password:
        return make_response(
            {
                'message': 'username/password is empty',
                'status': 'error'
            }, HTTPStatus.BAD_REQUEST
        )


def generate_password():
    import string
    import secrets

    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for _ in range(8))
    return password


@trace
def get_user_permissions(user_id):
    permissions = db.session.query(
        Permission
    ).join(
        RolePermissions
    ).join(
        UserRole, UserRole.role_id == RolePermissions.role_id
    ).filter(
        UserRole.user_id == user_id
    ).all()

    return permissions


@trace
def get_tokens(user_id, token=None):

    if token is None:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise ValueError('User not exists', user_id)

        permissions = [permission.code for permission in get_user_permissions(user.id)]
        is_superuser = user.is_superuser
    else:
        permissions = token.get('permissions', [])
        is_superuser = token.get('is_superuser', False)

    additional_claims = {
        'permissions': permissions,
        'is_superuser': is_superuser,
    }

    access_token = create_access_token(identity=user_id, additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=user_id, additional_claims=additional_claims)

    return access_token, refresh_token
