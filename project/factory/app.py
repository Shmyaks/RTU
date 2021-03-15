#it is base server
from flask import Flask
from flask_restful_swagger_3 import Api, swagger, get_swagger_blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os
from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.config["JWT_SECRET_KEY"] = "random_secret"

servers = [{"url": "http://localhost:5000"}]

api = Api(app, version='5', servers=servers, title="APP")
db = SQLAlchemy(app)
jwt = JWTManager(app)

SWAGGER_URL = '/api/doc'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'swagger.json'  # Our API url (can of course be a local resource)


from req_handler import Factories_routes, Create_Factory

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


swagger_blueprint = get_swagger_blueprint(
    api.open_api_json,
    swagger_prefix_url=SWAGGER_URL,
    swagger_url=API_URL,
    title='Factory service', version='1', servers=servers)


api.add_resource(Create_Factory, '/create_factory')
api.add_resource(Factories_routes, '/factory')

db.create_all()

app.register_blueprint(swagger_blueprint)

if __name__ == '__main__':
    manager.run()
    app.run(host='0.0.0.0',debug=True, port = 5003)

