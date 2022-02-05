from flask import Blueprint
from flasgger import swag_from

blueprint = Blueprint('role', __name__, url_prefix='/api/v1')


@swag_from('/docs/role_list.yml')
@blueprint.route('/role', methods=('GET',))
async def get_role_list():
    pass


@blueprint.route('/role', methods=('POST',))
async def create_role():
    pass


@blueprint.route('/role/<uuid:id>', methods=('GET',))
async def get_role_by_id():
    pass


@blueprint.route('/role/<uuid:id>', methods=('PUT',))
async def change_role():
    pass


@blueprint.route('/role/<uuid:id>', methods=('DELETE',))
async def delete_role():
    pass


@blueprint.route('/assign_role', methods=('POST',))
async def assign_role():
    pass


@blueprint.route('/check_permissions', methods=('GET',))
async def check_permissions():
    pass
