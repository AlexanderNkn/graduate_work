import datetime
import uuid

from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import INET, UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db
from models.base import BaseModel


class UserRole(BaseModel):
    __tablename__ = 'users_roles'

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, default=uuid.uuid4)  # noqa: E501
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('roles.id', ondelete='CASCADE'), nullable=False, default=uuid.uuid4)  # noqa: E501


def create_partition_user_sign_in(target, connection, **kw) -> None:
    """Creation partition by users_sign_in."""
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "users_sign_in_h0"
        PARTITION OF users_sign_in FOR VALUES WITH (MODULUS 5, REMAINDER 0)
        """
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "users_sign_in_h1"
        PARTITION OF users_sign_in FOR VALUES WITH (MODULUS 5, REMAINDER 1)
        """
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "users_sign_in_h2"
        PARTITION OF users_sign_in FOR VALUES WITH (MODULUS 5, REMAINDER 2)
        """
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "users_sign_in_h3"
        PARTITION OF users_sign_in FOR VALUES WITH (MODULUS 5, REMAINDER 3)
        """
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "users_sign_in_h4"
        PARTITION OF users_sign_in FOR VALUES WITH (MODULUS 5, REMAINDER 4)
        """
    )


class User(BaseModel):
    __tablename__ = 'users'

    username = db.Column(db.VARCHAR(255), nullable=False, unique=True)
    pwd_hash = db.Column(db.VARCHAR(255))
    is_superuser = db.Column(db.BOOLEAN(), default=False)
    data_joined = db.Column(db.TIMESTAMP(), default=datetime.datetime.now())
    terminate_date = db.Column(db.TIMESTAMP())

    roles = db.relationship('Role', secondary=UserRole.__tablename__, lazy=True)

    def __repr__(self):
        return f'{self.username}'

    @hybrid_property
    def password(self):
        return self.pwd_hash

    @password.setter  # type: ignore
    def password(self, value):
        """Store the password as a hash for security."""
        self.pwd_hash = generate_password_hash(value)

    def check_password(self, value):
        return check_password_hash(self.pwd_hash, value)


class UserData(BaseModel):
    __tablename__ = 'users_data'

    user_id = db.Column(db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship(User, backref=db.backref('users_datas', lazy=True))

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


class SocialAccount(BaseModel):
    __tablename__ = 'social_account'

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship(User, backref=db.backref('social_accounts', lazy=True))

    social_id = db.Column(db.Text, nullable=False)
    social_name = db.Column(db.Text, nullable=False)

    __table_args__ = (db.UniqueConstraint('social_id', 'social_name', name='social_pk'),)

    def __repr__(self):
        return f'<SocialAccount {self.social_name}:{self.user_id}>'


class UserSignIn(BaseModel):
    __tablename__ = 'users_sign_in'
    __table_args__ = (
        UniqueConstraint('id', 'user_id'),
        {
            'postgresql_partition_by': 'HASH(user_id)',
            'listeners': [('after_create', create_partition_user_sign_in)],
        }
    )

    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, primary_key=True
    )
    logined_by = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_agent = db.Column(db.Text)

    user = db.relationship(User, lazy=True, uselist=False)

    def __repr__(self):
        return f'<UserSignIn {self.user_id}:{self.logined_by}>'

    @classmethod
    def add_user_sign_in(cls, user_agent, logined_by=None, user=None, user_id=None):

        user_sign_in_data = {
            'user_agent': str(user_agent),
            'logined_by': logined_by,
            'user_id': user_id,
        }
        if user:
            user_sign_in_data['user'] = user

        user_sign_in = UserSignIn(**user_sign_in_data)
        db.session.add(user_sign_in)
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
