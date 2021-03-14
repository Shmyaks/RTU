#it is base server
from flask import Flask
from flask_restful_swagger_3 import Api, swagger, get_swagger_blueprint, register_schema
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

servers = [{"url": "http://localhost:5000"}]

api = Api(app, servers = servers)
db = SQLAlchemy(app)
jwt = JWTManager(app)

from req_handler import Purchase_routes, User_registration, User_routes, User_categories_routes, User_login, Admin_Shop, Shop_routes, CategorySHOP_routes, Product_routes, Shop_buy, Admin_Factories

api.add_resource(Purchase_routes, "/purchase")
api.add_resource(User_registration, '/register')
api.add_resource(User_routes, '/user/<int:user_id>')
api.add_resource(User_login,'/login')
api.add_resource(User_categories_routes, '/user/own_categories')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)

