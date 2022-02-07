import uvicorn
from asgiref.wsgi import WsgiToAsgi
from flasgger import Swagger
from flask import Flask
from flask_jwt_extended import JWTManager

from api.v1 import auth, role
from core import config
from core.config import SWAGGER_CONFIG
from core.logger import LOGGING
from db import postgres
# import models.users

app = Flask(__name__)
app.register_blueprint(auth.blueprint)
app.register_blueprint(role.blueprint)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{config.POSTGRE_USER}:{config.POSTGRE_PASSWORD}" + \
                                        f"@{config.POSTGRE_HOST}:{config.POSTGRE_PORT}/{config.POSTGRE_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# engine = create_engine("postgresql+psycopg2://scott:tiger@host/dbname")

postgres.db.init_app(app)
app.app_context().push()
postgres.db.create_all()

swagger_config = SWAGGER_CONFIG
Swagger(app, config=swagger_config, template_file='swagger_doc.yml')

app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config.JWT_ACCESS_TOKEN_EXPIRES
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = config.JWT_REFRESH_TOKEN_EXPIRES
app.config["JWT_ERROR_MESSAGE_KEY"] = "message"
jwt = JWTManager(app)

asgi_app = WsgiToAsgi(app)


if __name__ == '__main__':
    uvicorn.run(
        'main:asgi_app',
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        log_config=LOGGING
    )
