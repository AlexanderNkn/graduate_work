from models.users import UserData, UserSignIn
from extensions import ma


class UserDataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserData


class UserSignInSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserSignIn
        fields = ("user_id", "logined_by", "user_agent")


user_data_schema = UserDataSchema()

user_sign_in_schema = UserSignInSchema()
users_sign_in_schema = UserSignInSchema(many=True)
