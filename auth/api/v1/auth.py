from flask import Blueprint
from flask import request, make_response
from models.users import User

from db.postgres import db as db
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity, jwt_required
# from flask_jwt_extended import set_access_cookies

blueprint = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@blueprint.route('/register', methods=('POST',))
async def register():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
    elif request.method == 'GET':
        username = request.args.get('username')
        password = request.args.get('password')

    if not username or not password:
        return make_response(
            {
                "message": "username/password is empty",
                "status": "error"
            }, 400)

    user = User.query.filter_by(username=username).first()
    if user is not None:
        return make_response(
            {
                "message": "username already used",
                "status": "error"
            }, 400)

    user = User(username=username, pwd_hash=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return make_response(
            {
                "message": "User register",
                "status": "success"
            }, 200)


@blueprint.route('/login', methods=('POST',))
async def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        response = make_response(
            {
                "message": "username/password is empty",
                "status": "error"
            }, 400)
        return response

    user = User.query.filter_by(username=username).first()
    if user is None:
        return make_response(
            {
                "message": "user is not exist",
                "status": "error"
            }, 401)

    if not check_password_hash(user.pwd_hash, password):
        return make_response(
            {
                "message": "username/password are not valid",
                "status": "error"
            }, 401)

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
        }, 200)
    # set_access_cookies(response, access_token)

    return response


@blueprint.route('/logout', methods=('POST',))
@jwt_required()
async def logout():
    response = make_response({"message": "logout successful"})
    # unset_jwt_cookies(response)
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
        }, 200)


@blueprint.route('/change_password/<uuid:user_id>', methods=('PATCH',))
async def change_password():
    pass


@blueprint.route('/add_personal_data/<uuid:user_id>', methods=('POST',))
async def add_personal_data():
    pass


@blueprint.route('/change_personal_data/<uuid:user_id>', methods=('PATCH',))
async def change_personal_data():
    pass


@blueprint.route('/delete_personal_data/<uuid:user_id>', methods=('DELETE',))
async def delete_personal_data():
    pass


@blueprint.route('/login_history/<uuid:user_id>')
async def get_login_history():
    pass
