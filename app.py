from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from dotenv import load_dotenv

from db import db
from ma import ma
from resources.course import Course, CourseList
from resources.category import Category

load_dotenv('.env', verbose=True)

app = Flask(__name__)
app.config.from_object('default_config')

api = Api(app)
db.init_app(app)

api.add_resource(Course, '/course/<string:slug>')
api.add_resource(CourseList, '/courses')
api.add_resource(Category, '/category/<string:slug>')

jwt = JWTManager(app)
migrate = Migrate(app, db, render_as_batch=True)

if __name__ == '__main__':
    ma.init_app(app)
    app.run(port=5000)
