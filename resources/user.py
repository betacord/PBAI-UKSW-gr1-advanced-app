from hmac import compare_digest

from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token

from models.user import UserModel
from schemas.user import UserSchema

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls) -> any:
        user = user_schema.load(request.get_json())

        if UserModel.find_by_username(user.username):
            return {'message': f'User with username {user.username} already exists'}, 400

        try:
            user.save()
            return {'message': 'User created successfully'}, 202
        except Exception as e:
            return {'message': e}, 500


class UserLogin(Resource):
    @classmethod
    def post(cls) -> any:
        user_data = user_schema.load(request.get_json())
        user = UserModel.find_by_username(user_data.username)

        if user and compare_digest(user.password, user_data.password):
            access_token = create_access_token(identity=user.id, fresh=True)

            return {'access_token': access_token}, 200

        return {'message': 'Invalid credentials'}, 401
