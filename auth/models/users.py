from auth.db.postgres import db as db
from .base import BaseModel
import datetime

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import INET

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash


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

    @hybrid_property
    def password(self):
        return self.pwd_hash

    @password.setter
    def password(self, value):
        """Store the password as a hash for security."""
        self.pwd_hash = generate_password_hash(value)

    def check_password(self, value):
        return check_password_hash(self.pwd_hash, value)


class UserData(BaseModel):
    __tablename__ = 'users_data'
    # __table_args__ = ({"schema": "users"})

    user_id = db.Column(db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    first_name = db.Column(db.TEXT())
    last_name = db.Column(db.TEXT())
    email = db.Column(db.TEXT())
    birth_date = db.Column(db.TIMESTAMP())
    phone = db.Column(db.TEXT())
    city = db.Column(db.TEXT())

    def __repr__(self):
        return f'{self.first_name} {self.last_name}'


class UserDevice(BaseModel):
    __tablename__ = 'users_device'
    # __table_args__ = ({"schema": "users"})

    user_id = db.Column(db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    ip = db.Column(INET())
    device_key = db.Column(db.TEXT())
    user_agent = db.Column(db.TEXT())

    def __repr__(self):
        return f'{self.ip} {self.user_agent}'


# class UserWithRoles(BaseModel):
#     roles = relation(
#         Role,
#         secondary=UserRole.__tablename__,
#         viewonly=True
#     )
#
