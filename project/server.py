#it is base server
from flask import Flask, Blueprint
from flask_restful_swagger_3 import Api, swagger, get_swagger_blueprint, register_schema
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.config["JWT_SECRET_KEY"] = "random_secret"

api = Api(app)
schema_marshmallow = Marshmallow(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)

from req_handler import routes_purchase, User_registration, User_routes, User_login, add_purchase

api.add_resource(routes_purchase, '/purchase/<int:purchase_id>')
api.add_resource(add_purchase, "/purchase")
api.add_resource(User_registration, '/register')
api.add_resource(User_routes, '/user/<int:user_id>')
api.add_resource(User_login,'/login')

db.create_all()
if __name__ == '__main__':
    app.run(debug=True)

