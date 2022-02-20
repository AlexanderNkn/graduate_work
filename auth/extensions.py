from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_caching import Cache

jwt = JWTManager()
db = SQLAlchemy()
ma = Marshmallow()
cache = Cache()
