from http import HTTPStatus

from flask import Blueprint, make_response, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from extensions import db
from models import User, UserData
from schemas import user_data_schema
from utils.common import permission_required, get_tokens


blueprint = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


def check_empty_user_password(username, password):
    if not username or not password:
        return make_response(
            {
                "message": "username/password is empty",
                "status": "error"
            }, HTTPStatus.BAD_REQUEST)
    return


@blueprint.route('/register', methods=('POST',))
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    response = check_empty_user_password(username, password)
    if response:
        return response

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
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    response = check_empty_user_password(username, password)
    if response:
        return response

    user = User.query.filter_by(username=username).first()
    if user is None:
        return make_response(
            {
                "message": "user is not exist",
                "status": "error"
            }, HTTPStatus.UNAUTHORIZED)

    if not user.check_password(password):
        return make_response(
            {
                "message": "username or password are not correct",
                "status": "error"
            }, HTTPStatus.UNAUTHORIZED)

    access_token, refresh_token = get_tokens(user.id)
    response = make_response(
        {
            "message": "JWT tokens were generated successfully",
            "status": "success",
            "tokens": {
                "access_token": access_token,
                "refresh_token": refresh_token
              }
        }, HTTPStatus.OK)

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

    try:
        access_token, refresh_token = get_tokens(user_id, token)
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
@permission_required(permission='change_password')
def change_password(user_id):
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


@blueprint.route('/personal_data/<uuid:user_id>', methods=('GET',))
@permission_required(permission='get_personal_data')
def get_personal_data(user_id):
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

    return make_response(user_data_schema.dump(user_data), HTTPStatus.OK)


@blueprint.route('/add_personal_data/<uuid:user_id>', methods=('POST',))
@permission_required(permission='add_personal_data')
def add_personal_data(user_id):
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
@permission_required(permission='change_personal_data')
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
@permission_required(permission='delete_personal_data')
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
