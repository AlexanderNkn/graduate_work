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
