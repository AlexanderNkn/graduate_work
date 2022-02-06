from sqlalchemy import Column, VARCHAR, Text, ForeignKey

from .base import BaseModel


class Role(BaseModel):
    __tablename__ = 'users'

    code = Column(VARCHAR(255), nullable=False, unique=True)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return f'({self.code}) {self.description}'


class UserRole(BaseModel):
    __tablename__ = 'users_roles'

    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    role_id = Column(ForeignKey('roles.id', ondelete='CASCADE'), nullable=False, index=True)
