import uvicorn
from asgiref.wsgi import WsgiToAsgi
from flasgger import Swagger
from flask import Flask

from api.v1 import auth, role
from core.config import SWAGGER_CONFIG
from core.logger import LOGGING

app = Flask(__name__)
app.register_blueprint(auth.blueprint)
app.register_blueprint(role.blueprint)

swagger_config = SWAGGER_CONFIG
Swagger(app, config=swagger_config, template_file='swagger_doc.yml')

asgi_app = WsgiToAsgi(app)


if __name__ == '__main__':
    uvicorn.run(
        'main:asgi_app',
        host='0.0.0.0',
        port=5000,
        log_config=LOGGING
    )
