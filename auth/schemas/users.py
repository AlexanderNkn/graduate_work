from models.users import UserData
from extensions import ma


class UserDataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserData


user_data_schema = UserDataSchema()
