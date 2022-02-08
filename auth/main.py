import uvicorn
from asgiref.wsgi import WsgiToAsgi
from flasgger import Swagger
from flask import Flask
import click

from api.v1 import auth, role
from core.config import SWAGGER_CONFIG
from core.logger import LOGGING

app = Flask(__name__)
app.register_blueprint(auth.blueprint)
app.register_blueprint(role.blueprint)

swagger_config = SWAGGER_CONFIG
Swagger(app, config=swagger_config, template_file='swagger_doc.yml')

asgi_app = WsgiToAsgi(app)


@app.cli.command("create-superuser")
@click.argument("name", "password")
def create_superuser(name, password):
    user = User(username=name, pwd_hash=generate_password_hash(password), is_superuser=True)
    db.session.add(user)

    admin_role = Role.query.filter_by(code="admin").first()
    user_role = UserRole(user_id=user.id, role_id=admin_role.id)
    db.session.add(user_role)
    db.session.commit()


if __name__ == '__main__':
    uvicorn.run(
        'main:asgi_app',
        host='0.0.0.0',
        port=5000,
        log_config=LOGGING
    )
