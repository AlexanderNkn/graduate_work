from extensions import db

from .base import BaseModel


class Role(BaseModel):
    __tablename__ = 'roles'

    code = db.Column(db.VARCHAR(255), nullable=False, unique=True)
    description = db.Column(db.Text, default='')

    def __repr__(self):
        return f'({self.code}) {self.description}'


class UserRole(BaseModel):
    __tablename__ = 'users_roles'

    user_id = db.Column(db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    role_id = db.Column(db.ForeignKey('roles.id', ondelete='CASCADE'), nullable=False)
