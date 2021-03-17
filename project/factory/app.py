#it is base server
from flask import Flask
from flask_restful_swagger_3 import Api, swagger, get_swagger_blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os
from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


servers = [{"url": "http://localhost:5002"}]

api = Api(app, version='5', servers=servers, title="APP")
db = SQLAlchemy(app)
jwt = JWTManager(app)

SWAGGER_URL = '/api/doc'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'swagger.json'  # Our API url (can of course be a local resource)

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}

scheduler = BackgroundScheduler(jobstores = jobstores)#This is sheduler

from req_handler import Factories_routes, Craft

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
        title='Example', version='1', servers=servers)



api.add_resource(Factories_routes, '/factory')
api.add_resource(Craft, '/factory/craft')

db.create_all()

app.register_blueprint(swagger_blueprint, url_prefix=swagger_blueprint_url_prefix)

if __name__ == '__main__':
    manager.run()
    scheduler.start()
    app.run(host='0.0.0.0', debug=True, port = 5002)

