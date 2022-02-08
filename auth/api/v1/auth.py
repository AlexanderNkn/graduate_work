from flask import Blueprint
from flask import request, make_response
from http import HTTPStatus
from models.users import User, UserData, UserDevice

from db.postgres import db as db
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

# from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
# from flask_jwt_extended import set_access_cookies

from utils import common
from utils.common import perm_required

blueprint = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@blueprint.route('/register', methods=('POST',))
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return make_response(
            {
                "message": "username/password is empty",
                "status": "error"
            }, HTTPStatus.BAD_REQUEST)

    user = User.query.filter_by(username=username).first()
    if user is not None:
        return make_response(
            {
                "message": "username already used",
                "status": "error"
            }, HTTPStatus.BAD_REQUEST)

    user = User(username=username, pwd_hash=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return make_response(
            {
                "message": "User register",
                "status": "success"
            }, HTTPStatus.OK)


@blueprint.route('/login', methods=('POST',))
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        response = make_response(
            {
                "message": "username/password is empty",
                "status": "error"
            }, HTTPStatus.BAD_REQUEST)
        return response

    user = User.query.filter_by(username=username).first()
    if user is None:
        return make_response(
            {
                "message": "user is not exist",
                "status": "error"
            }, HTTPStatus.UNAUTHORIZED)

    if not check_password_hash(user.pwd_hash, password):
        return make_response(
            {
                "message": "username/password are not valid",
                "status": "error"
            }, HTTPStatus.UNAUTHORIZED)

    access_token, refresh_token = common.get_tokens(user.id)
    response = make_response(
        {
            "message": "JWT tokens were generated successfully",
            "status": "success",
            "tokens": {
                "access_token": access_token,
                "refresh_token": refresh_token
              }
        }, HTTPStatus.OK)
    # set_access_cookies(response, access_token)

    return response


@blueprint.route('/logout', methods=('POST',))
@jwt_required()
def logout():
    response = make_response({"message": "logout successful"})
    return response


@blueprint.route('/refresh_token', methods=('POST',))
@jwt_required(refresh=True)
def refresh_token():
    user_id = get_jwt_identity()
    token = get_jwt()

    # access_token = create_access_token(identity=identity)
    try:
        access_token, refresh_token = common.get_tokens(user_id, token)
    except ValueError:
        return make_response(
                {
                    "message": "user is not exist",
                    "status": "error"
                }, HTTPStatus.UNAUTHORIZED)

    return make_response(
        {
            "message": "JWT tokens were generated successfully",
            "status": "success",
            "tokens": {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        }, HTTPStatus.OK)


@blueprint.route('/change_password/<uuid:user_id>', methods=('PATCH',))
@perm_required(permission='change_password')
def change_password(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return make_response(
            {
                "message": "user not found",
                "status": "error"
            }, HTTPStatus.UNAUTHORIZED)
    old_password = request.json.get('old_password')
    new_password = request.json.get('new_password')

    if not check_password_hash(user.pwd_hash, old_password):
        return make_response(
            {
                "message": "username/password are not valid",
                "status": "error"
            }, HTTPStatus.UNAUTHORIZED)

    user.pwd_hash = generate_password_hash(new_password)
    db.session.add(user)
    db.session.commit()
    return make_response(
        {
            "message": "password changed successfully",
            "status": "success"
        }, HTTPStatus.OK)


@blueprint.route('/add_personal_data/<uuid:user_id>', methods=('POST',))
@perm_required(permission='add_personal_data')
def add_personal_data(user_id):
    # {
    #     "birth_date": "1970-10-8",
    #     "city": "Cambridge",
    #     "email": "matt@damon.com",
    #     "first_name": "Matt",
    #     "last_name": "Damon",
    #     "phone": 71234567
    # }

    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return make_response(
            {
                "message": "user not found",
                "status": "error"
            }, HTTPStatus.UNAUTHORIZED)

    # user_data = UserData.query.filter_by(id=user_id).first()
    # if user_data is None:
    user_data = UserData(user_id=user_id)

    for key in request.json:
        setattr(user_data, key, request.json[key])

    db.session.add(user_data)
    db.session.commit()
    return make_response(
        {
            "message": "user personal was data added successfully",
            "status": "success"
        }, HTTPStatus.OK)


@blueprint.route('/change_personal_data/<uuid:user_id>', methods=('PATCH',))
@perm_required(permission='change_personal_data')
def change_personal_data(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return make_response(
            {
                "message": "user not found",
                "status": "error"
            }, HTTPStatus.UNAUTHORIZED)

    user_data = UserData.query.filter_by(user_id=user_id).first()
    if user_data is None:
        user_data = UserData(user_id=user_id)

    for key in request.json:
        setattr(user_data, key, request.json[key])

    db.session.add(user_data)
    db.session.commit()
    return make_response(
        {
            "message": "user personal was data added successfully",
            "status": "success"
        }, HTTPStatus.OK)


@blueprint.route('/delete_personal_data/<uuid:user_id>', methods=('DELETE',))
@perm_required(permission='delete_personal_data')
def delete_personal_data(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return make_response(
            {
                "message": "user not found",
                "status": "error"
            }, HTTPStatus.UNAUTHORIZED)

    UserData.query.filter_by(user_id=user_id).delete()
    db.session.commit()

    return make_response(
        {
            "message": "user personal data was deleted successfully",
            "status": "success"
        }, HTTPStatus.OK)


@blueprint.route('/login_history/<uuid:user_id>')
@perm_required(permission='get_login_history')
def get_login_history(user_id):
    pass
