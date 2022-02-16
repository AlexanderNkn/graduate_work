from extensions import db
from models.base import BaseModel


class Permission(BaseModel):
    __tablename__ = 'permissions'

    code = db.Column(db.VARCHAR(255), nullable=False, unique=True)

    def __repr__(self):
        return f'({self.code}) {self.description}'


def create_permissions():
    permissions = [
        'users',
        'personal_data',
        'roles',
    ]

    for permission_code in permissions:
        permission = Permission.query.filter_by(code=permission_code).first()
        if not permission:
            db.session.add(Permission(code=permission_code))
    db.session.commit()
