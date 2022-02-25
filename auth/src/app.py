import os

import backoff
import click
import sentry_sdk
from flasgger import Swagger
from flask import Flask
from flask_migrate import init as init_db, migrate as migrate_db, upgrade as upgrade_db
from flask_migrate import downgrade as downgrade_db
from flask_opentracing import FlaskTracer
from jaeger_client import Config
from opentracing import global_tracer
from sentry_sdk.integrations.flask import FlaskIntegration
from sqlalchemy.exc import OperationalError

from core import config as default_config
from extensions import cache, db, jwt, ma, migrate, oauth

__all__ = ('create_app',)


def create_app(config=default_config) -> Flask:
    """Create a Flask app."""
    sentry_sdk.init(
        dsn=config.SENTRY_DSN,
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0,
    )
    app = Flask(__name__, instance_relative_config=True)

    configure_blueprints(app)
    configure_db(app, config=config.PostgresSettings())
    configure_migrate(app)
    configure_cache(app, config=config.RedisSettings())
    configure_jwt(app, config=config.JWTSettings())
    configure_ma(app)
    configure_oauth(app, config=config.OAuthGoogleSettings())
    configure_swagger(app, config=config.SWAGGER_CONFIG)
    configure_cli(app)
    configure_errors(app, event=sentry_sdk.last_event_id)
    configure_jaeger(app, jaeger_config=config.JAEGER_CONFIG)
    configure_before_request(app, config)

    return app


def configure_db(app, config) -> None:
    app.config.from_object(config)
    db.init_app(app)
    app.app_context().push()


@backoff.on_exception(backoff.expo, OperationalError, max_time=300)
def configure_migrate(app) -> None:
    migrations_dir = os.path.join(os.path.dirname(__file__), 'migrations')
    migrate.init_app(app=app, db=db, directory=migrations_dir)
    if not os.path.exists(migrations_dir):
        init_db(directory=migrations_dir)
        migrate_db(message='Initial migration')
    upgrade_db()


def configure_cache(app, config) -> None:
    app.config.from_object(config)
    cache.init_app(app)


def configure_jwt(app, config) -> None:
    app.config.from_object(config)
    jwt.init_app(app)

    from error_handlers import register_jwt_errors
    register_jwt_errors(config)


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


def configure_swagger(app, config) -> None:
    Swagger(app, config=config, template_file='definitions.yml')


def configure_blueprints(app) -> None:
    from api.v1.auth import blueprint as auth_blueprint
    from api.v1.role import blueprint as role_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(role_blueprint)


def configure_cli(app):

    @app.cli.command('recreate-database')
    def initdb():
        downgrade_db()
        upgrade_db()

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


def configure_errors(app, event) -> None:
    from error_handlers import register_500_error, register_429_error
    register_500_error(app, sentry_event=event)
    register_429_error(app)


def configure_before_request(app, config) -> None:
    from utils.limits import check_request_id, check_rate_limit

    @app.before_request
    def before_request():
        check_request_id()
        check_rate_limit(limit=config.REQUEST_LIMIT_PER_MINUTE)


def configure_jaeger(app, jaeger_config) -> None:

    def setup_jaeger():
        config = Config(
            config=jaeger_config,
            service_name='auth',
            validate=True,
        )
        # Jaeger tracer is a global object unlike flask instance created via create_app().
        # Once initialized it should be invoked using global_tracer() when create flask app next time.
        tracer = config.initialize_tracer() or global_tracer()
        return tracer

    FlaskTracer(tracer=setup_jaeger, app=app)
