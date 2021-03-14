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
app.config["JWT_SECRET_KEY"] = "random_secret"

servers = [{"url": "http://localhost:5000"}]

api = Api(app, servers = servers)
db = SQLAlchemy(app)
jwt = JWTManager(app)


from req_handler import Admin_Factories

db.create_all()

api.add_resource(Admin_Factories, '/create_factory')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port = 5003)

