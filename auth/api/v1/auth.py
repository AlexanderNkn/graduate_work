import uuid
from calendar import timegm
from datetime import datetime, timezone
from http import HTTPStatus

from flask import Blueprint, current_app, make_response, request, url_for
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from extensions import db, jwt_redis_blocklist, oauth
from models import SocialAccount, User, UserData, UserSignIn
from schemas import user_data_schema, users_sign_in_schema
from utils.common import check_empty_user_password, generate_password, get_tokens
from utils.permissions import permission_required

blueprint = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@blueprint.route('/login_google')
def login_google():
    redirect_uri = url_for('auth.auth_google', _external=True)
    return oauth.google.authorize_redirect(redirect_uri, access_type='offline')


@blueprint.route('/auth_google')
def auth_google():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token)
    user_email = user['email']

    social_account = SocialAccount.query.filter_by(social_id=user_email, social_name='google').first()
    if social_account is None:
        user_id = uuid.uuid4()
        user = User(id=user_id, username=str(user_id), password=generate_password())
        social_account = SocialAccount(user=user, social_id=user_email, social_name='google')

        db.session.add(social_account)
        db.session.commit()
    else:
        user_id = social_account.user_id

    access_token, refresh_token = get_tokens(user_id)
    response = make_response(
        {
            "message": "JWT tokens were generated successfully",
            "status": "success",
            "tokens": {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        }, HTTPStatus.OK)

    UserSignIn.add_user_sign_in(request.user_agent, user_id=user_id)

    return response


@blueprint.route('/register', methods=('POST',))
def register():
    """
    Endpoint to register new account
    ---
    tags:
    - REGISTRATION
    description: Create new user account
    requestBody:
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Credentials'
          example:
            username: yandex
            password: 12345
    responses:
      200:
        description: Successfull registration
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Response'
            example:
              status: success
              message: New account was registered successfully
      400:
        description: Registration failed
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Response'
            example:
              status: error
              message: The username is already in use
    """
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
    """
    Endpoint for user login
    ---
    tags:
    - LOGIN
    description: Get JWT tokens after login
    requestBody:
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Credentials'
          example:
            username: yandex
            password: 12345
    responses:
      200:
        description: A pair of access/refresh tokens
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Response'
              properties:
                tokens:
                  $ref: '#/components/schemas/Token'
            example:
              status: success
              message: JWT tokens were generated successfully
              tokens:
                access_token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
                refresh_token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
      401:
        description: Unauthorized access
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Response'
            example:
              status: error
              message: username or password are not correct
    """
    username = request.json and request.json.get('username')
    password = request.json and request.json.get('password')

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

    UserSignIn.add_user_sign_in(request.user_agent, user=user)

    return response


@blueprint.route('/logout', methods=('POST',))
@jwt_required()
def logout():
    """
    Endpoint to logout user
    ---
    tags:
    - LOGOUT
    description: User logout
    responses:
      200:
        description: Logout successfull
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Response'
            example:
              status: success
              message: User logout successfull
      401:
        $ref: '#/components/responses/Unauthorized'
    security:
    - jwt_auth:
      - write:admin,subscriber,member
    """
    jti = get_jwt()['jti']
    jwt_redis_blocklist.set(jti, '', timeout=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])
    response = make_response(
        {
          'status': 'success',
          'message': 'User logout successfull',
        }, HTTPStatus.OK)
    return response


@blueprint.route('/refresh-token', methods=('POST',))
@jwt_required(refresh=True)
def refresh_token():
    """
    Endoint to refresh expired tokens
    ---
    tags:
    - REFRESH_TOKEN
    description: Refresh expired tokens
    responses:
      200:
        description: New tokens were generated
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Response'
            example:
              status: success
              message: New tokens were generated
      401:
        $ref: '#/components/responses/Unauthorized'
    security:
    - jwt_auth:
      - write:admin,subscriber,member
    """
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

    now = timegm(datetime.now(tz=timezone.utc).utctimetuple())
    access_expired = token['iat'] + current_app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds()

    if access_expired < now:
        UserSignIn.add_user_sign_in(request.user_agent, user_id=user_id)

    return make_response(
        {
            "message": "JWT tokens were generated successfully",
            "status": "success",
            "tokens": {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        }, HTTPStatus.OK)


@blueprint.route('/change-password/<uuid:user_id>', methods=('PATCH',))
@permission_required('users')
def change_password(user_id):
    """
    Endpoint to change forgotten password
    ---
    tags:
    - CHANGE_PASSWORD
    description: Change user password
    parameters:
    - description: User id to change history
      in: path
      name: user_id
      required: true
      schema:
        type: string
    requestBody:
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Passwords'
          example:
            old_password: 12345
            new_password: 678910
    responses:
      200:
        description: Password changed successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Response'
            example:
              status: success
              message: password changed successfully
      401:
        $ref: '#/components/responses/Unauthorized'
      403:
        $ref: '#/components/responses/Forbidden'
      404:
        $ref: '#/components/responses/NotFound'
    security:
    - jwt_auth:
      - write:admin,subscriber,member
      - read:admin,subscriber,member
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return make_response(
            {
                "message": "resource not found",
                "status": "error"
            }, HTTPStatus.NOT_FOUND)
    old_password = request.json.get('old_password', '')
    new_password = request.json.get('new_password', '')

    if not user.check_password(old_password):
        return make_response(
            {
                "message": "username/password are not valid",
                "status": "error"
            }, HTTPStatus.UNAUTHORIZED)

    response = check_empty_user_password(user_id, new_password)
    if response:
        return response

    user.password = new_password
    db.session.add(user)
    db.session.commit()
    return make_response(
        {
            "message": "password changed successfully",
            "status": "success"
        }, HTTPStatus.OK)


@blueprint.route('/personal-data/<uuid:user_id>', methods=('GET',))
@permission_required('personal_data')
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


@blueprint.route('/personal-data/<uuid:user_id>', methods=('POST',))
@permission_required('personal_data')
def add_personal_data(user_id):
    """
    Endpoint for user to add personal data
    ---
    tags:
    - ADD_PERSONAL_DATA
    description: Additional info about user
    requestBody:
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/UserData'
          example:
            first_name: Matt
            last_name: Damon
            email: matt@damon.com
            birth_date: 1970-10-08
            phone: +71234567
            city: Cambridge
    parameters:
    - name: user_id
      in: path
      required: true
      description: User id to add/change/delete personal data
      schema:
        type: string
    responses:
      201:
        description: User data was added successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Response'
            example:
              status: success
              message: user personal was data added successfully
      401:
        $ref: '#/components/responses/Unauthorized'
      403:
        $ref: '#/components/responses/Forbidden'
      404:
        $ref: '#/components/responses/NotFound'
    security:
      - jwt_auth:
        - write:admin,subscriber,member
        - read:admin,subscriber,member
    """
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


@blueprint.route('/personal-data/<uuid:user_id>', methods=('PATCH',))
@permission_required('personal_data')
def change_personal_data(user_id):
    """
    Endpoint for user to change data
    ---
    tags:
    - CHANGE_PERSONAL_DATA
    description: Additional info about user
    requestBody:
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/UserData'
          example:
            first_name: Matt
            last_name: Damon
            email: matt@damon.com
            birth_date: 1970-10-08
            phone: +71234567
            city: Cambridge
    parameters:
    - name: user_id
      in: path
      required: true
      description: User id to add/change/delete personal data
      schema:
        type: string
    responses:
      200:
        description: User data was changed successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Response'
            example:
              status: success
              message: user personal data was changed successfully
      401:
        $ref: '#/components/responses/Unauthorized'
      403:
        $ref: '#/components/responses/Forbidden'
      404:
        $ref: '#/components/responses/NotFound'
    security:
    - jwt_auth:
      - write:admin,subscriber,member
      - read:admin,subscriber,member
    """
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


@blueprint.route('/login-history/<uuid:user_id>')
@permission_required('personal_data')
def get_login_history(user_id):
    """
    Endpoint to get history of user logouts
    ---
    tags:
    - LOGIN_HISTORY
    description: info about user login
    parameters:
    - name: user_id
      in: path
      required: true
      description: User id to view login history
      schema:
        type: string
    responses:
      200:
        description: User login history is available
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Response'
              properties:
                history:
                  $ref: '#/components/schemas/UserLoginHistory'
            example:
              status: success
              message: user login history is available
              history:
                - user_id: 29e124d6-b7d2-4a81-82d5-82d2dc3685ae
                  user_agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36
                  logined_by: 2022-02-18T16:17:01.089822
                - user_id: 29e124d6-b7d2-4a81-82d5-82d2dc3685ae
                  user_agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36
                  logined_by: 2022-02-14T16:05:16.298483
      401:
        $ref: '#/components/responses/Unauthorized'
      403:
        $ref: '#/components/responses/Forbidden'
      404:
        $ref: '#/components/responses/NotFound'
    security:
    - jwt_auth:
      - write:admin,subscriber,member
      - read:admin,subscriber,member
    """
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    user_sign_ins = UserSignIn.query.filter_by(user_id=user_id).\
        order_by(UserSignIn.logined_by.desc()).paginate(page, per_page, error_out=False)
    return make_response(
        {
            "history": users_sign_in_schema.dump(user_sign_ins.items),
            "message": "user login history is available",
            "status": "success",
        },
        HTTPStatus.OK)


@blueprint.route('/personal-data/<uuid:user_id>', methods=('DELETE',))
@permission_required('personal_data')
def delete_personal_data(user_id):
    """
    Endpoint to delete user personal data
    ---
    tags:
    - DELETE_PERSONAL_DATA
    description: Additional info about user
    parameters:
    - name: user_id
      in: path
      required: true
      description: User id to add/change/delete personal data
      schema:
        type: string
    responses:
      204:
        description: User data was deleted successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Response'
            example:
              status: success
              message: user personal data was deleted successfully
      401:
        $ref: '#/components/responses/Unauthorized'
      403:
        $ref: '#/components/responses/Forbidden'
      404:
        $ref: '#/components/responses/NotFound'
    security:
    - jwt_auth:
      - write:admin,subscriber,member
      - read:admin,subscriber,member
    """
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
