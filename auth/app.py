import backoff
import click
import sentry_sdk
from flasgger import Swagger
from flask import Flask, request
from flask_opentracing import FlaskTracer
from jaeger_client import Config
from sentry_sdk.integrations.flask import FlaskIntegration
from sqlalchemy.exc import OperationalError

from core import config as default_config
from extensions import db, jwt, ma

__all__ = ('create_app',)


def create_app(config=None) -> Flask:
    """Create a Flask app."""
    sentry_sdk.init(
        dsn=default_config.SENTRY_DSN,
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0,
    )
    app = Flask(__name__, instance_relative_config=True)

    config = config or default_config
    configure_before_request(app)
    configure_blueprints(app)
    configure_db(app, config=config.PostgresSettings())
    configure_jwt(app, config=config.JWTSettings())
    configure_ma(app)
    configure_swagger(app)
    configure_cli(app)
    configure_errors(app, event=sentry_sdk.last_event_id)
    configure_jaeger(app)

    return app


@backoff.on_exception(backoff.expo, OperationalError, max_time=300)
def configure_db(app, config) -> None:
    app.config.from_object(config)
    db.init_app(app)
    app.app_context().push()
    db.create_all()


def configure_jwt(app, config) -> None:
    app.config.from_object(config)
    jwt.init_app(app)


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


def configure_errors(app, event) -> None:
    from error_handlers import register_500_error
    register_500_error(app, sentry_event=event)


def configure_before_request(app) -> None:

    @app.before_request
    def before_request():
        if not request.headers.get('X-Request-Id'):
            raise RuntimeError('request id is requred')


def configure_jaeger(app) -> None:

    def setup_jaeger():
        config = Config(
            config=default_config.JAEGER_CONFIG,
            service_name='auth',
            validate=True,
        )
        tracer = config.initialize_tracer()
        if tracer is None:
            Config._initialized = False
            tracer = config.initialize_tracer()
        return tracer

    FlaskTracer(tracer=setup_jaeger, app=app)
