from models.roles import Role
from extensions import ma


class RoleSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Role
        fields = ('id', 'code', 'description')


role_schema = RoleSchema()
