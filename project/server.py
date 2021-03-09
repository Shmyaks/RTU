#it is base server
from flask import Flask, Blueprint
from flask_restful_swagger_3 import Api, swagger, get_swagger_blueprint, register_schema
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.config["JWT_SECRET_KEY"] = "random_secret"

api = Api(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)

from req_handler import Purchase_routes, User_registration, User_routes, User_categories_routes, User_login, Admin_Shop, Shop_routes, CategorySHOP_routes, Product_routes, Shop_buy 


api.add_resource(Purchase_routes, "/purchase")

api.add_resource(User_registration, '/register')
api.add_resource(User_routes, '/user/<int:user_id>')
api.add_resource(User_login,'/login')
api.add_resource(User_categories_routes, '/user/own_categories')

api.add_resource(Admin_Shop, '/create_shop')
api.add_resource(Shop_routes, '/shop/<int:shop_id>')
api.add_resource(CategorySHOP_routes, '/shop/categories')
api.add_resource(Product_routes, '/shop/products')
api.add_resource(Shop_buy, '/shop/buy')

db.create_all()
if __name__ == '__main__':
    app.run(debug=True)

