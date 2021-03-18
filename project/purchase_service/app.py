#it is base server
from flask import Flask
from flask_restful_swagger_3 import Api, get_swagger_blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate
import os
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

servers = [{"url": "http://localhost:80"}]

api = Api(app, servers = servers)
db = SQLAlchemy(app)

SWAGGER_URL = '/api/doc'  # URL for exposing Swagsger UI (without trailing '/')
API_URL = 'swagger.json'  # Our API url (can of course be a local resource)

from req_handler import Purchase_routes, User_routes, User_categories_routes, User_registration, Purchase_get_by_shop

app.config.setdefault('SWAGGER_BLUEPRINT_URL_PREFIX', '/api/purchase/doc')
swagger_blueprint_url_prefix = app.config.get('SWAGGER_BLUEPRINT_URL_PREFIX', '')

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

with app.app_context():
    swagger_blueprint = get_swagger_blueprint(
        api.open_api_json,
        swagger_prefix_url=SWAGGER_URL,
        swagger_url=API_URL,
        title='Purchase service', version='1', servers=servers)

api.add_resource(Purchase_routes, "/api/purchase")
api.add_resource(User_routes, '/api/user/<int:user_id>')
api.add_resource(User_categories_routes, '/api/user/own_categories')
api.add_resource(User_registration, '/api/user/register')
api.add_resource(Purchase_get_by_shop, "/api/purchases")

app.register_blueprint(swagger_blueprint,  url_prefix=swagger_blueprint_url_prefix)

if __name__ == '__main__':
    manager.run()
    app.run(host='0.0.0.0', debug=False, port=5000)

