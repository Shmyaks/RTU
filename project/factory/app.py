#it is base server
from flask import Flask
from flask_restful_swagger_3 import Api, swagger, get_swagger_blueprint
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate
import os
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


servers = [{"url": "http://localhost:80"}]

api = Api(app, version='5', servers=servers, title="APP")
db = SQLAlchemy(app)

SWAGGER_URL = '/api/doc'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'swagger.json'  # Our API url (can of course be a local resource)

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}

scheduler = BackgroundScheduler(jobstores = jobstores)#This is sheduler

from req_handler import Factories_routes, Craft

app.config.setdefault('SWAGGER_BLUEPRINT_URL_PREFIX', '/api/factory/doc')
swagger_blueprint_url_prefix = app.config.get('SWAGGER_BLUEPRINT_URL_PREFIX', '')

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

with app.app_context():
    swagger_blueprint = get_swagger_blueprint(
        api.open_api_json,
        swagger_prefix_url=SWAGGER_URL,
        swagger_url=API_URL,
        title='Factory service', version='1', servers=servers)


api.add_resource(Factories_routes, '/api/factory')
api.add_resource(Craft, '/api/factory/craft')

app.register_blueprint(swagger_blueprint, url_prefix=swagger_blueprint_url_prefix)

db.create_all()

if __name__ == '__main__':
    manager.run()
    scheduler.start()
    app.run(host='0.0.0.0', debug=True, port = 5002)

