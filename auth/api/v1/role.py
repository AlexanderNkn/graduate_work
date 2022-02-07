from flask import Blueprint
from flasgger import swag_from

blueprint = Blueprint('role', __name__, url_prefix='/api/v1')


@blueprint.route('/role', methods=('GET',))
async def get_role_list():
    pass


@blueprint.route('/role', methods=('POST',))
async def create_role():
    pass


@blueprint.route('/role/<uuid:role_id>')
async def get_role_by_id():
    pass


@blueprint.route('/role/<uuid:role_id>', methods=('PATCH',))
async def change_role():
    pass


@blueprint.route('/role/<uuid:role_id>', methods=('DELETE',))
async def delete_role():
    pass


@blueprint.route('/assign_roles', methods=('POST',))
async def assign_roles():
    pass


@blueprint.route('/check_permissions', methods=('POST',))
async def check_permissions():
    pass
