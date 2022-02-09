from flask import Blueprint
from flask import request, make_response
from http import HTTPStatus
from auth.models.users import User, UserData

from auth.extensions import db
# from werkzeug.security import check_password_hash
# from werkzeug.security import generate_password_hash

from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity, jwt_required
# from flask_jwt_extended import set_access_cookies

blueprint = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@blueprint.route('/register', methods=('POST',))
async def register():
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
                "message": "The username is already in use",
                "status": "error"
            }, HTTPStatus.BAD_REQUEST)

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return make_response(
            {
                "message": "New account was registered successfully",
                "status": "success"
            }, HTTPStatus.OK)


@blueprint.route('/login', methods=('POST',))
async def login():
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

    # if not check_password_hash(user.pwd_hash, password):
    if not user.check_password(password):
        return make_response(
            {
                "message": "username or password are not correct",
                "status": "error"
            }, HTTPStatus.UNAUTHORIZED)

    access_token = create_access_token(identity="example_user")
    refresh_token = create_refresh_token(identity="example_user")
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
async def logout():
    response = make_response(
        {
            "message": "User logout successful",
            "status": "success"
        }, HTTPStatus.OK)
    return response


@blueprint.route('/refresh_token', methods=('POST',))
@jwt_required(refresh=True)
async def refresh_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    # refresh_token = create_refresh_token(identity=identity)
    return make_response(
        {
            "message": "JWT tokens were generated successfully",
            "status": "success",
            "tokens": {
                "access_token": access_token,
                # "refresh_token": refresh_token,
              }
        }, HTTPStatus.OK)


@blueprint.route('/change_password/<uuid:user_id>', methods=('PATCH',))
@jwt_required()
async def change_password(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return make_response(
            {
                "message": "resource not found",
                "status": "error"
            }, HTTPStatus.NOT_FOUND)
    old_password = request.json.get('old_password')
    new_password = request.json.get('new_password')

    if not user.check_password(old_password):
        return make_response(
            {
                "message": "username/password are not valid",
                "status": "error"
            }, HTTPStatus.UNAUTHORIZED)

    user.password = new_password
    db.session.add(user)
    db.session.commit()
    return make_response(
        {
            "message": "password changed successfully",
            "status": "success"
        }, HTTPStatus.OK)


@blueprint.route('/add_personal_data/<uuid:user_id>', methods=('POST',))
@jwt_required()
async def add_personal_data(user_id):
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
                "message": "resource not found",
                "status": "error"
            }, HTTPStatus.NOT_FOUND)

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
@jwt_required()
async def change_personal_data(user_id):
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
@jwt_required()
async def delete_personal_data(user_id):
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
@jwt_required()
async def get_login_history(user_id):
    pass
