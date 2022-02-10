from flasgger import Swagger
from flask import Flask

from core import config as default_config
from extensions import db, jwt

__all__ = ('create_app',)


def create_app(config=None) -> Flask:
    """Create a Flask app."""
    app = Flask(__name__, instance_relative_config=True)

    config = config or default_config
    configure_blueprints(app)
    configure_db(app, config=config.PostgresSettings())
    configure_jwt(app, config=config.JWTSettings())
    configure_swagger(app)

    return app


def configure_db(app, config) -> None:
    app.config.from_object(config)
    db.init_app(app)
    app.app_context().push()
    # db.drop_all()
    db.create_all()


def configure_jwt(app, config) -> None:
    app.config.from_object(config)
    jwt.init_app(app)


def configure_swagger(app) -> None:
    Swagger(app, config=default_config.SWAGGER_CONFIG, template_file='swagger_doc.yml')


def configure_blueprints(app) -> None:
    from api.v1.auth import blueprint as auth_blueprint
    from api.v1.role import blueprint as role_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(role_blueprint)
