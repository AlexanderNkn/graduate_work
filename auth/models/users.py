from db.postgres import db as db
from .base import BaseModel
import datetime

# from sqlalchemy.ext.hybrid import hybrid_property

# from werkzeug.security import check_password_hash
# from werkzeug.security import generate_password_hash


class User(BaseModel):
    __tablename__ = 'users'
    # __table_args__ = ({"schema": "users"})

    username = db.Column(db.VARCHAR(255), nullable=False, unique=True)
    pwd_hash = db.Column(db.VARCHAR(255))
    is_superuser = db.Column(db.BOOLEAN(), default=False)
    data_joined = db.Column(db.TIMESTAMP(), default=datetime.datetime.now())
    terminate_date = db.Column(db.TIMESTAMP())

    def __repr__(self):
        return f'{self.username}'

#     # @hybrid_property
#     def password(self):
#         return self._password
#
#     @password.setter
#     def password(self, value):
#         """Store the password as a hash for security."""
#         self._password = generate_password_hash(value)
#
#     def check_password(self, value):
#         return check_password_hash(self.password, value)


# class UserWithRoles(BaseModel):
#     roles = relation(
#         Role,
#         secondary=UserRole.__tablename__,
#         viewonly=True
#     )
#
