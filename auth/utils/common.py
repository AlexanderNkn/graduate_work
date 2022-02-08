
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


def get_tokens(user=None, token=None):
    if user is None and token is None:
        raise ValueError('User or token must be fill')

    if user is not None:
        identity = user.id
        perms = [perm.code for perm in get_user_permissions(user.id)]
        is_superuser = user.is_superuser
    else:
        verify_jwt_in_request()
        identity = get_jwt_identity()
        claims = get_jwt()
        perms = claims.get('perms', [])
        is_superuser = claims.get('is_superuser', False)

    additional_claims = {
        'perms': perms,
        'is_superuser': is_superuser,
    }

    access_token = create_access_token(identity=identity, additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=identity, additional_claims=additional_claims)

    return access_token, refresh_token

# def admin_required():
#     def wrapper(fn):
#         @wraps(fn)
#         def decorator(*args, **kwargs):
#             verify_jwt_in_request()
#             claims = get_jwt()
#             if claims["is_administrator"]:
#                 return fn(*args, **kwargs)
#             else:
#                 return jsonify(msg="Admins only!"), 403
#
#         return decorator
