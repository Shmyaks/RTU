#it is base server
from flask import Flask
from flask_restful_swagger_3 import Api, swagger, get_swagger_blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

servers = [{"url": "http://localhost:5000"}]

api = Api(app, servers = servers)
db = SQLAlchemy(app)
jwt = JWTManager(app)

SWAGGER_URL = '/api/doc'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'swagger.json'  # Our API url (can of course be a local resource)

from req_handler import Purchase_routes, User_routes, User_categories_routes, User_registration

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

swagger_blueprint = get_swagger_blueprint(
    api.open_api_json,
    swagger_prefix_url=SWAGGER_URL,
    swagger_url=API_URL,
    title='Purchase service', version='1', servers=servers)

api.add_resource(Purchase_routes, "/purchase")
api.add_resource(User_routes, '/user/<int:user_id>')
api.add_resource(User_categories_routes, '/user/own_categories')
api.add_resource(User_registration, '/register')

db.create_all()

app.register_blueprint(swagger_blueprint)


if __name__ == '__main__':
    manager.run()
    app.run(host='0.0.0.0', debug=True, port=5000)

