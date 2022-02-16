from extensions import db
from models.base import BaseModel


class RolePermissions(BaseModel):
    __tablename__ = 'roles_permissions'

    role_id = db.Column(db.ForeignKey('roles.id', ondelete='CASCADE'), nullable=False)
    perm_id = db.Column(db.ForeignKey('permissions.id', ondelete='CASCADE'), nullable=False)


class Role(BaseModel):
    __tablename__ = 'roles'

    code = db.Column(db.VARCHAR(255), nullable=False, unique=True)
    description = db.Column(db.Text, default='')

    permissions = db.relationship('Permission', secondary=RolePermissions.__table__, lazy='dynamic')

    def __repr__(self):
        return f'({self.code}) {self.description}'

