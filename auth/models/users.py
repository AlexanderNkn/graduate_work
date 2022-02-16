import datetime

from sqlalchemy.dialects.postgresql import INET, UUID
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db
from models.base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

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

    user_id = db.Column(db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
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

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    ip = db.Column(INET())
    device_key = db.Column(db.TEXT())
    user_agent = db.Column(db.TEXT())

    def __repr__(self):
        return f'{self.ip} {self.user_agent}'


class UserSignIn(BaseModel):
    __tablename__ = 'users_sign_in'

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    logined_by = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_agent = db.Column(db.Text)

    def __repr__(self):
        return f'<UserSignIn {self.user_id}:{self.logined_by}>'

    @staticmethod
    def add_user_sign_in(user, user_agent, logined_by=None):
        # from flask import request
        # request.headers.get('User-Agent')
        # request.user_agent
        pass
