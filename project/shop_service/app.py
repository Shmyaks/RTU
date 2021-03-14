#it is base server
from flask import Flask
from flask_restful_swagger_3 import Api, swagger, get_swagger_blueprint, register_schema
from flask_sqlalchemy import SQLAlchemy                                                  
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


api = Api(app)
db = SQLAlchemy(app)

from req_handler import Admin_Shop, Shop_routes, CategorySHOP_routes, Product_routes, Shop_buy



api.add_resource(Admin_Shop, '/shop/create_shop')
api.add_resource(Shop_routes, '/shop/<int:shop_id>')
api.add_resource(CategorySHOP_routes, '/shop/categories')
api.add_resource(Product_routes, '/shop/products')
api.add_resource(Shop_buy, '/shop/buy')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port = 5001)

