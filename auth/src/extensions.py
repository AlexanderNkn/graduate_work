from authlib.integrations.flask_client import OAuth
from flask_caching import Cache
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

jwt = JWTManager()
db = SQLAlchemy()
ma = Marshmallow()
oauth = OAuth()
cache = Cache()

# cache alias for flask-jwt-extended
jwt_redis_blocklist = cache
