from extensions import db
from models.base import BaseModel


class Permission(BaseModel):
    __tablename__ = 'permissions'

    code = db.Column(db.VARCHAR(255), nullable=False, unique=True)

    def __repr__(self):
        return f'{self.code}'

