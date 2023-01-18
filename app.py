from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from dotenv import load_dotenv

from db import db
from ma import ma
from resources.course import Course

load_dotenv('.env', verbose=True)

app = Flask(__name__)
app.config.from_object('default_config')

api = Api(app)
db.init_app(app)

api.add_resource(Course, '/course/<string:slug>')

jwt = JWTManager(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    ma.init_app(app)
    app.run(port=5000)
