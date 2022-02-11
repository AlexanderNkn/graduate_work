import uuid
from http import HTTPStatus

from flask import Blueprint, make_response, request
from flask_jwt_extended import jwt_required

from extensions import db
from models import Role, UserRole, User
from schemas import role_schema

blueprint = Blueprint('role', __name__, url_prefix='/api/v1')


@blueprint.route('/role', methods=('GET', ))
def get_role_list():
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
@jwt_required()
def create_role():
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
@jwt_required()
def get_role_by_id(role_id):
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
@jwt_required()
def change_role(role_id):
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
@jwt_required()
def delete_role(role_id):
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


@blueprint.route('/assign_roles', methods=('POST',))
@jwt_required()
def assign_roles():
    pass


@blueprint.route('/check_permissions', methods=('POST',))
@jwt_required()
def check_permissions():
    user_id = uuid.UUID(request.json.get('user_id'))
    role_ids = [uuid.UUID(role_id) for role_id in request.json.get('role_ids')]
    user_role = UserRole.query.join(User).filter(User.id.in_(
        [user_id])).join(Role).filter(Role.id.in_(role_ids)).first()
    if user_role is None:
        make_response(
            {
                "message": "user is not foud or hasn't any roles",
                "status": "success"
            }, HTTPStatus.NOT_FOUND)
    return make_response(
        {
            "message": "permissions checked",
            "status": "success",
            "has_permissions": True
        }, HTTPStatus.OK)
