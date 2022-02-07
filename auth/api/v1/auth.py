from flask import Blueprint

blueprint = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@blueprint.route('/register', methods=('POST',))
async def register():
    pass


@blueprint.route('/login', methods=('POST',))
async def login():
    pass


@blueprint.route('/logout', methods=('POST',))
async def logout():
    pass


@blueprint.route('/refresh_token', methods=('POST',))
async def refresh_token():
    pass


@blueprint.route('/change_password/<uuid:user_id>', methods=('PATCH',))
async def change_password():
    pass


@blueprint.route('/personal_data/<uuid:user_id>', methods=('POST',))
async def add_personal_data():
    pass


@blueprint.route('/personal_data/<uuid:user_id>', methods=('PATCH',))
async def change_personal_data():
    pass


@blueprint.route('/personal_data/<uuid:user_id>', methods=('DELETE',))
async def delete_personal_data():
    pass


@blueprint.route('/login_history/<uuid:user_id>')
async def get_login_history():
    pass
