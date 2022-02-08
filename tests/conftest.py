import pytest
# import pytest_asyncio

from flask import Flask
from api.v1 import auth, role

from .settings import settings


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(auth.blueprint)
    app.register_blueprint(role.blueprint)

    init_jwt(app)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def create_db(db_url):
    import psycopg2
    from psycopg2 import Error
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user=settings.dsn.user,
                                      # пароль, который указали при установке PostgreSQL
                                      password=settings.dsn.password,
                                      host=settings.dsn.host,
                                      port=settings.dsn.port)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        sql_drop_database = f'DROP DATABASE IF EXISTS {settings.dsn.dbname}'
        cursor.execute(sql_drop_database)
        sql_create_database = f'CREATE DATABASE {settings.dsn.dbname}'
        cursor.execute(sql_create_database)
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")


@pytest.fixture
def db(app):
    db_url = f"postgresql+psycopg2://{settings.dsn.user}:{settings.dsn.password}" + \
              f"@{settings.dsn.host}:{settings.dsn.port}/{settings.dsn.dbname}"
    # create_db(db_url)

    from db.postgres import db

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)
    app.app_context().push()
    db.drop_all()
    db.create_all()

    return db


def init_jwt(app):
    from flask_jwt_extended import JWTManager

    app.config["JWT_SECRET_KEY"] = settings.jwt.JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = settings.jwt.JWT_ACCESS_TOKEN_EXPIRES
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = settings.jwt.JWT_REFRESH_TOKEN_EXPIRES
    app.config["JWT_ERROR_MESSAGE_KEY"] = "message"
    jwt = JWTManager(app)
