from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from authlib.integrations.flask_client import OAuth

jwt = JWTManager()
db = SQLAlchemy()
ma = Marshmallow()
oauth = OAuth()
