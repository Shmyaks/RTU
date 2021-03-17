#it is base server
from flask import Flask
from flask_restful_swagger_3 import Api, swagger, get_swagger_blueprint, register_schema
from flask_sqlalchemy import SQLAlchemy                                                  
import os
from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate

app = Flask(__name__)

servers = [{"url": "http://localhost:5000"}]

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

api = Api(app)
db = SQLAlchemy(app)

SWAGGER_URL = '/api/doc'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'swagger.json'  # Our API url (can of course be a local resource)

from req_handler import Create_shop, Shop_routes, CategorySHOP_routes, Product_routes, Shop_buy, Checks, Checks_products, Shop_product, Delivery

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

app.config.setdefault('SWAGGER_BLUEPRINT_URL_PREFIX', '/shop/swagger')
swagger_blueprint_url_prefix = app.config.get('SWAGGER_BLUEPRINT_URL_PREFIX', '')

with app.app_context():
    swagger_blueprint = get_swagger_blueprint(
        api.open_api_json,
        swagger_prefix_url=SWAGGER_URL,
        swagger_url=API_URL,
        title='Shop service', version='1', servers=servers)

api.add_resource(Create_shop, '/shop/create_shop')
api.add_resource(Shop_routes, '/shop/<int:shop_id>')
api.add_resource(CategorySHOP_routes, '/shop/categories')
api.add_resource(Product_routes, '/shop/products')
api.add_resource(Shop_buy, '/shop/buy')
api.add_resource(Checks, '/shop/checks')
api.add_resource(Checks_products, '/shop/checks/purchase')
api.add_resource(Shop_product, '/shop/product/search')
api.add_resource(Delivery, '/shop/delivery')

app.register_blueprint(swagger_blueprint,  url_prefix=swagger_blueprint_url_prefix)

db.create_all()

if __name__ == '__main__':
    manager.run()
    app.run(host='0.0.0.0', debug=True, port=5000)

