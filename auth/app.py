import click
from flasgger import Swagger
from flask import Flask

from core import config as default_config
from databases import redis_db
from extensions import db, jwt, ma, oauth

__all__ = ('create_app',)


def create_app(config=None) -> Flask:
    """Create a Flask app."""
    app = Flask(__name__, instance_relative_config=True)

    config = config or default_config
    configure_blueprints(app)
    configure_db(app, config=config.PostgresSettings())
    configure_jwt(app, config=config.JWTSettings())
    configure_ma(app)
    configure_oauth(app, config=config.OAuthGoogleSettings())
    configure_swagger(app)
    configure_cli(app)
    configure_redis(config=config.RedisSettings())

    return app


def configure_db(app, config) -> None:
    app.config.from_object(config)
    db.init_app(app)
    app.app_context().push()
    db.create_all()


def configure_jwt(app, config) -> None:
    app.config.from_object(config)
    jwt.init_app(app)

    # Callback function to check if a JWT exists in the redis blocklist
    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token_in_redis = redis_db.jwt_redis_blocklist().get(jti)
        return token_in_redis is not None

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


def configure_oauth(app, config) -> None:
    app.config.from_object(config)

    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.init_app(app)
    oauth.register(
        name='google',
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )


def configure_swagger(app) -> None:
    Swagger(app, config=default_config.SWAGGER_CONFIG, template_file='definitions.yml')


def configure_redis(config) -> None:
    redis_db.redis = redis_db.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0, decode_responses=True)


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

    @app.cli.command('load-init-data')
    def load_init_data():
        from init_data import PERMISSIONS, ROLES
        from models import Permission, Role

        objects = []

        for permission_info in PERMISSIONS:
            permission = Permission.query.filter_by(code=permission_info['code']).first()
            if not permission:
                permission = Permission(**permission_info)
                objects.append(permission)

        for role_info in ROLES:
            permissions = role_info.pop('permissions', [])
            role = Role.query.filter_by(code=role_info['code']).first()
            if not role:
                role = Role(**role_info)
                for permission in permissions:
                    role.permissions.append(Permission.query.filter_by(code=permission).first())
                role.permissions = [permission for permission in role.permissions if permission]
                objects.append(role)

        db.session.add_all(objects)
        db.session.commit()
