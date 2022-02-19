import backoff
import click
import sentry_sdk
from flasgger import Swagger
from flask import Flask
from flask_opentracing import FlaskTracer
from jaeger_client import Config
from opentracing import global_tracer
from sentry_sdk.integrations.flask import FlaskIntegration
from sqlalchemy.exc import OperationalError

from core import config as default_config
from extensions import db, jwt, ma

__all__ = ('create_app',)


def create_app(config=default_config) -> Flask:
    """Create a Flask app."""
    sentry_sdk.init(
        dsn=config.SENTRY_DSN,
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0,
    )
    app = Flask(__name__, instance_relative_config=True)

    configure_before_request(app, config)
    configure_blueprints(app)
    configure_db(app, config=config.PostgresSettings())
    configure_jwt(app, config=config.JWTSettings())
    configure_ma(app)
    configure_swagger(app, config=config.SWAGGER_CONFIG)
    configure_cli(app)
    configure_errors(app, event=sentry_sdk.last_event_id)
    configure_jaeger(app, jaeger_config=config.JAEGER_CONFIG)

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
