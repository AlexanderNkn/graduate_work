from models.permissions import Permission
from extensions import ma


class PermissionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Permission


permission_schema = PermissionSchema()
