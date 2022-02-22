import uuid
from http import HTTPStatus

from flask import Blueprint, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db, cache
from models import Role, UserRole, Permission
from schemas import role_schema, user_role_schema, permission_schema
from utils.permissions import permission_required, has_permission

blueprint = Blueprint('role', __name__, url_prefix='/auth-api/v1')


@blueprint.route('/permission', methods=('GET', ))
@permission_required('roles')
def get_permission_list():
    """
    Endpoint to get all permissions
    ---
    tags:
      - PERMISSION_LIST
    description: List of all available permissions
    responses:
      200:
        description: List of permissions is available
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                $ref: '#/components/schemas/Permission'
              example:
                - id: a9c6e8da-f2bf-458a-978b-d2f50a031451
                  code: admin
                  description: unlimited access to all actions
                - id: 7cf56926-054c-4522-ac6f-d9f5d0e9d18e
                  code: subscriber
                  description: account without paying for registered users
                - id: 7166fd5f-a4e4-45f0-952c-78d0297c7b03
                  code: member
                  description: account with payment options
      401:
        $ref: '#/components/responses/Unauthorized'
      403:
        $ref: '#/components/responses/Forbidden'
      404:
        $ref: '#/components/responses/NotFound'
    """
    permissions = Permission.query.all()
    if permissions is None:
        return make_response({
            "message": "Permission list is empty",
            "status": "success",
        }, HTTPStatus.NO_CONTENT)
    return make_response(
        {
            "status": "success",
            "permissions": [permission_schema.dump(permission) for permission in permissions]
        }, HTTPStatus.OK)


@blueprint.route('/role', methods=('GET', ))
@permission_required('roles')
def get_role_list():
    """
    Endpoint to get all roles
    ---
    tags:
      - ROLE_LIST
    description: List of all available roles
    responses:
      200:
        description: List of roles is available
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                $ref: '#/components/schemas/Role'
              example:
                - id: a9c6e8da-f2bf-458a-978b-d2f50a031451
                  code: admin
                  description: unlimited access to all actions
                - id: 7cf56926-054c-4522-ac6f-d9f5d0e9d18e
                  code: subscriber
                  description: account without paying for registered users
                - id: 7166fd5f-a4e4-45f0-952c-78d0297c7b03
                  code: member
                  description: account with payment options
      401:
        $ref: '#/components/responses/Unauthorized'
      403:
        $ref: '#/components/responses/Forbidden'
      404:
        $ref: '#/components/responses/NotFound'
    """
    roles = Role.query.all()
    if roles is None:
        return make_response({
            "message": "Role list is empty",
            "status": "success",
        }, HTTPStatus.NO_CONTENT)
    return make_response(
        {
            "status": "success",
            "roles": [role_schema.dump(role) for role in roles]
        }, HTTPStatus.OK)


@blueprint.route('/role', methods=('POST',))
@permission_required('roles')
def create_role():
    """
    Endpoint to create new role
    ---
    tags:
      - CREATE_ROLE
    description: Create new role
    requestBody:
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Role'
          example:
            code: admin
            description: unlimited access to all actions
    responses:
      201:
        description: List of roles is available
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Response'
              properties:
                role:
                  $ref: '#/components/schemas/Role'
            example:
              status: success
              message: New role was created
              role:
                id: a9c6e8da-f2bf-458a-978b-d2f50a031451
                code: admin
                description: unlimited access to all actions
      401:
        $ref: '#/components/responses/Unauthorized'
      403:
        $ref: '#/components/responses/Forbidden'
    security:
    - jwt_auth:
      - write:admin
      - read:admin
    """
    role_code = request.json.get('code')
    role_description = request.json.get('description')
    if not role_code or not role_description:
        return make_response(
            {
                "message": "role code/role description is empty",
                "status": "error"
            }, HTTPStatus.BAD_REQUEST)
    role = Role.query.filter_by(code=role_code).first()
    if role is not None:
        return make_response(
            {
                "message": "role is already existed",
                "status": "error"
            }, HTTPStatus.BAD_REQUEST)
    role = Role(code=role_code, description=role_description)
    db.session.add(role)
    db.session.commit()
    return make_response(
        {
            "message": "Role created",
            "status": "success"
        }, HTTPStatus.CREATED)


@blueprint.route('/role/<uuid:role_id>', methods=('GET', ))
@permission_required('roles')
def get_role_by_id(role_id):
    """
    Get role detailes
    ---
    tags:
    - ROLE_DETAILS
    description: detailed info about role
    parameters:
    - name: role_id
      in: path
      required: true
      description: Role uuid
      schema:
        type: string
      example:
        role_id: a9c6e8da-f2bf-458a-978b-d2f50a031451
    responses:
      200:
        description: info about role is available
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Response'
              properties:
                role:
                  $ref: '#/components/schemas/Role'
            example:
              status: success
              message: info about role is available
              role:
                id: a9c6e8da-f2bf-458a-978b-d2f50a031451
                code: admin
                description: unlimited access to all actions
      401:
        $ref: '#/components/responses/Unauthorized'
      403:
        $ref: '#/components/responses/Forbidden'
      404:
        $ref: '#/components/responses/NotFound'
    """
    role = Role.query.filter_by(id=role_id).first()
    if role is None:
        return make_response(
            {
                "message": "Role is not found",
                "status": "error"
            }, HTTPStatus.NOT_FOUND)
    return make_response(
        {
            "status": "success",
            "role": role_schema.dump(role)
        }, HTTPStatus.OK)


@blueprint.route('/role/<uuid:role_id>', methods=('PATCH',))
@permission_required('roles')
def change_role(role_id):
    """
    Endpoint to change role
    ---
    tags:
    - CHANGE_ROLE_DETAILS
    description: change role info
    requestBody:
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Role'
          example:
            code: admin
            description: unlimited access to all actions
    parameters:
    - name: role_id
      in: path
      required: true
      description: Role uuid
      schema:
        type: string
      example:
        role_id: a9c6e8da-f2bf-458a-978b-d2f50a031451
    responses:
      200:
        description: info about role was changed successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Response'
              properties:
                role:
                  $ref: '#/components/schemas/Role'
            example:
              status: success
              message: info about role was changed successfully
              role:
                id: a9c6e8da-f2bf-458a-978b-d2f50a031451
                code: admin
                description: unlimited access to all actions
      401:
        $ref: '#/components/responses/Unauthorized'
      403:
        $ref: '#/components/responses/Forbidden'
      404:
        $ref: '#/components/responses/NotFound'
    """
    role = Role.query.filter_by(id=role_id).first()
    if role is None:
        return make_response(
            {
                "message": "Role is not found",
                "status": "error"
            }, HTTPStatus.NOT_FOUND)
    for key in request.json:
        setattr(role, key, request.json[key])
    db.session.add(role)
    db.session.commit()
    return make_response(
        {
            "message": "role data was changed sucessfully",
            "status": "success",
            "role": role_schema.dump(role)
        }, HTTPStatus.OK)


@blueprint.route('/role/<uuid:role_id>', methods=('DELETE',))
@permission_required('roles')
def delete_role(role_id):
    """
    Endpoint to delete role
    ---
    tags:
    - DELETE_ROLE
    description: delete role
    parameters:
    - name: role_id
      in: path
      required: true
      description: Role uuid
      schema:
        type: string
      example:
        role_id: a9c6e8da-f2bf-458a-978b-d2f50a031451
    responses:
      204:
        description: role was deleted successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Response'
            example:
              status: success
              message: role was deleted successfully
      401:
        $ref: '#/components/responses/Unauthorized'
      403:
        $ref: '#/components/responses/Forbidden'
      404:
        $ref: '#/components/responses/NotFound'
    security:
      - jwt_auth:
        - write:admin
        - read:admin
    """
    role = Role.query.filter_by(id=role_id).first()
    if role is None:
        return make_response(
            {
                "message": "Role is not found",
                "status": "error"
            }, HTTPStatus.NOT_FOUND)
    Role.query.filter_by(id=role_id).delete()
    db.session.commit()
    return make_response(
        {
            "message": "role was sucessfully deleted",
            "status": "success"
        }, HTTPStatus.NO_CONTENT)


@blueprint.route('/assign-roles', methods=('POST',))
@permission_required('roles')
def assign_roles():
    """
    Endpoint to assign roles to user
    ---
    tags:
      - ASSIGN_ROLES
    description: Assign roles to user
    requestBody:
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/UserRoleRequest'
          example:
            user_id: 7cd483e9-5888-40fd-813a-a382154bcfd2
            role_ids: [a9c6e8da-f2bf-458a-978b-d2f50a031451, 7cf56926-054c-4522-ac6f-d9f5d0e9d18e]
    responses:
      201:
        description: Roles were assigned successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Response'
              properties:
                user_roles:
                  $ref: '#/components/schemas/UserRoleResponse'
            example:
              status: success
              message: roles were assigned to user
              user_roles:
                - id: 4a73b964-af72-4801-aed9-113783561540
                  user_id: 7cd483e9-5888-40fd-813a-a382154bcfd2
                  role_id: a9c6e8da-f2bf-458a-978b-d2f50a031451
                - id: 0f55b9d8-f027-4766-9476-2b89e17c1854
                  user_id: 7cd483e9-5888-40fd-813a-a382154bcfd2
                  role_id: 7cf56926-054c-4522-ac6f-d9f5d0e9d18e
      401:
        $ref: '#/components/responses/Unauthorized'
      403:
        $ref: '#/components/responses/Forbidden'
      404:
        description: The specified resource was not found
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Response'
            examples:
              nouser:
                value:
                  status: error
                  message: user not found
              norole:
                value:
                  status: error
                  message: role not found
    security:
    - jwt_auth:
      - write:admin
      - read:admin
    """
    user_id = request.json.get('user_id')
    role_ids = request.json.get('role_ids')
    user_role_list = [UserRole(user_id=user_id, role_id=id) for id in role_ids]
    db.session.bulk_save_objects(user_role_list)
    db.session.commit()
    return make_response(
      {
          'message': 'roles were assigned to user',
          'status': 'success',
          'user_roles': [user_role_schema.dump(user_role) for user_role in user_role_list]
      }, HTTPStatus.CREATED)


@blueprint.route('/check-roles', methods=('POST',))
@permission_required('roles')
def check_roles():
    """
    Endpoint to check user roles
    ---
    tags:
      - CHECK_ROLES
    description: check if user belongs to specified roles
    requestBody:
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/UserRoleRequest'
          example:
            user_id: 7cd483e9-5888-40fd-813a-a382154bcfd2
            role_ids: [a9c6e8da-f2bf-458a-978b-d2f50a031451, 7cf56926-054c-4522-ac6f-d9f5d0e9d18e]
    responses:
      200:
        description: Roles were checked successfully
        content:
          application/json:
            schema:
              properties:
                status:
                  type: string
                message:
                  type: string
                has_roles:
                  type: boolean
            examples:
              approved:
                value:
                  status: success
                  message: roles were checked successfully
                  has_roles: true
              disapproved:
                value:
                  status: success
                  message: roles were checked successfully
                  has_roles: false
      401:
        $ref: '#/components/responses/Unauthorized'
      403:
        $ref: '#/components/responses/Forbidden'
      404:
        description: The specified resource was not found
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Response'
            examples:
              nouser:
                value:
                  status: error
                  message: user not found
              norole:
                value:
                  status: error
                  message: role not found
    security:
    - jwt_auth:
      - write:admin
      - read:admin
    """
    user_id = request.json.get('user_id')
    role_ids = request.json.get('role_ids')
    user_role = UserRole.query.filter_by(user_id=user_id).filter(UserRole.role_id.in_(role_ids)).first()
    if user_role is None:
        make_response(
            {
                "message": "user is not found or hasn't any roles",
                "status": "success",
                "has_roles": False
            }, HTTPStatus.NOT_FOUND)
    return make_response(
        {
            "message": "roles checked",
            "status": "success",
            "has_roles": True
        }, HTTPStatus.OK)


@blueprint.route('/check-permission', methods=('POST',))
@jwt_required()
@cache.cached(timeout=30)
def check_permission():
    """
    Endpoint to check user permissions
    ---
    tags:
      - CHECK_PERMISSION
    description: check if user belongs to specified permission
    requestBody:
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/UserRoleRequest'
          example:
            permission: 'users'
    responses:
      200:
        description: Permission was checked successfully
        content:
          application/json:
            schema:
              properties:
                status:
                  type: string
                message:
                  type: string
                has_permission:
                  type: boolean
            examples:
              approved:
                value:
                  status: success
                  message: permission was checked successfully
                  has_permission: true
              disapproved:
                value:
                  status: success
                  message: permission was checked successfully
                  has_permission: true
      401:
        $ref: '#/components/responses/Unauthorized'
      404:
        description: The specified resource was not found
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Response'
            examples:
              nouser:
                value:
                  status: error
                  message: user not found
              nopermission:
                value:
                  status: error
                  message: permission not found
    """
    permission = request.json.get('permission')
    token_user_id = uuid.UUID(get_jwt_identity())

    return make_response(
        {
            "message": "permissions checked",
            "status": "success",
            "has_permission": has_permission(permission=permission, token_user_id=token_user_id)
        }, HTTPStatus.OK)
