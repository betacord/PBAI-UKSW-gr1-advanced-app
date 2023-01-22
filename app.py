from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from dotenv import load_dotenv
from marshmallow import ValidationError

from db import db
from ma import ma
from resources.course import Course, CourseList
from resources.category import Category, CategoryList
from resources.user import UserLogin, UserRegister

load_dotenv('.env', verbose=True)

app = Flask(__name__)
app.config.from_object('default_config')

api = Api(app)
db.init_app(app)


@app.errorhandler(ValidationError)
def handle_marshmallow_error(err: any) -> any:
    return jsonify(err.messages), 401


api.add_resource(Course, '/course/<string:slug>')
api.add_resource(CourseList, '/courses')
api.add_resource(Category, '/category/<string:slug>')
api.add_resource(CategoryList, '/categories')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')

jwt = JWTManager(app)
migrate = Migrate(app, db, render_as_batch=True)

if __name__ == '__main__':
    ma.init_app(app)
    app.run(port=5000)
