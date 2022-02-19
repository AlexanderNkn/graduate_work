import click
from flasgger import Swagger
from flask import Flask

from core import config as default_config
from extensions import db, jwt, ma

__all__ = ('create_app',)


def create_app(config=None) -> Flask:
    """Create a Flask app."""
    app = Flask(__name__, instance_relative_config=True)

    config = config or default_config
    configure_blueprints(app)
    configure_db(app, config=config.PostgresSettings())
    configure_jwt(app, config=config.JWTSettings())
    configure_ma(app)
    configure_swagger(app)
    configure_cli(app)

    return app


def configure_db(app, config) -> None:
    app.config.from_object(config)
    db.init_app(app)
    app.app_context().push()
    db.create_all()


def configure_jwt(app, config) -> None:
    app.config.from_object(config)
    jwt.init_app(app)

    from flask import jsonify

    @jwt.expired_token_loader
    def _expired_token_callback(_expired_jwt_header, _expired_jwt_data):
        return jsonify({config.JWT_ERROR_MESSAGE_KEY: "Token has expired", "status": "error"}), 401

    @jwt.invalid_token_loader
    def _invalid_token_callback(error_string):
        return jsonify({config.JWT_ERROR_MESSAGE_KEY: error_string, "status": "error"}), 422

    @jwt.unauthorized_loader
    def _unauthorized_callback(error_string):
        return jsonify({config.JWT_ERROR_MESSAGE_KEY: error_string, "status": "error"}), 401

    @jwt.needs_fresh_token_loader
    def _needs_fresh_token_callback(jwt_header, jwt_data):
        return jsonify({config.error_msg_key: "Fresh token required", "status": "error"}), 401

    @jwt.revoked_token_loader
    def _revoked_token_callback(jwt_header, jwt_data):
        return jsonify({config.JWT_ERROR_MESSAGE_KEY: "Token has been revoked", "status": "error"}), 401


def configure_ma(app) -> None:
    ma.init_app(app)


def configure_swagger(app) -> None:
    Swagger(app, config=default_config.SWAGGER_CONFIG, template_file='definitions.yml')


def configure_blueprints(app) -> None:
    from api.v1.auth import blueprint as auth_blueprint
    from api.v1.role import blueprint as role_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(role_blueprint)


def configure_cli(app):

    @app.cli.command('recreate-database')
    def initdb():
        db.drop_all()
        db.create_all()

    @app.cli.command('create-superuser')
    @click.argument('name')
    @click.argument('password')
    def create_superuser(name, password):
        from models import Role, User, UserRole
        user = User(username=name, password=password, is_superuser=True)
        db.session.add(user)

        admin_role = Role.query.filter_by(code='admin').first()
        if admin_role:
            user_role = UserRole(user_id=user.id, role_id=admin_role.id)
            db.session.add(user_role)
        db.session.commit()
