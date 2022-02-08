from sqlalchemy import Column, VARCHAR, Text, ForeignKey

from .base import BaseModel


class Permission(BaseModel):
    __tablename__ = 'perms'

    code = Column(VARCHAR(255), nullable=False, unique=True)

    def __repr__(self):
        return f'{self.code}'


class RolePerms(BaseModel):
    __tablename__ = 'roles_perms'

    role_id = Column(ForeignKey('roles.id', ondelete='CASCADE'), nullable=False, index=True)
    perm_id = Column(ForeignKey('perms.id', ondelete='CASCADE'), nullable=False, index=True)
