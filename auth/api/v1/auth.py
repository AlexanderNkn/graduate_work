from flask import Blueprint

blueprint = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@blueprint.route('/register')
async def register():
    pass


@blueprint.route('/login', methods=('POST',))
async def login():
    pass


@blueprint.route('/logout')
async def logout():
    pass


@blueprint.route('/refresh_token')
async def refresh_token():
    pass


@blueprint.route('/change_credentials')
async def change_credentials():
    pass


@blueprint.route('/add_personal_data')
async def add_personal_data():
    pass


@blueprint.route('/change_personal_data')
async def change_personal_data():
    pass


@blueprint.route('/delete_personal_data')
async def delete_personal_data():
    pass


@blueprint.route('/login_history')
async def get_login_history():
    pass
