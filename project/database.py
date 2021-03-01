from __main__ import db
from datetime import datetime
from flask_restful_swagger_3 import Schema
from werkzeug.security import generate_password_hash, check_password_hash

class Users(db.Model, Schema):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(32), nullable = True)
    second_name = db.Column(db.String(32), nullable = True)
    login = db.Column(db.String(32), nullable = True)
    password = db.Column(db.String())
    date_registration = db.Column(db.DateTime, default = datetime.utcnow, nullable = True)
    purchases = db.relationship("Purchase", lazy='dynamic')

    type = "object"
    properties = {
        'id': {
            'type': 'integer',
            'format': 'int64'
        },
        'first_name': {
            'type': 'string'
        },
        'second_name': {
            'type': 'string',
        },
        'date_registration':{
            'type': 'datetime'
        },
        'login': {
            'type': 'string'
        }
    }

    def check_password(self, password: str):
        return check_password_hash(self.password, password)

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.first_name = kwargs.get('first_name')
        self.second_name = kwargs.get('second_name')
        self.login = kwargs.get('login')
        self.password = generate_password_hash(kwargs.get('password'), method='sha256')
        
    def __repr__(self):
        return '<user_id %r>' % self.user_id
    

class Purchase(db.Model, Schema):
    purchase_id = db.Column(db.Integer, primary_key = True)
    purchase_name = db.Column(db.String(64), nullable = True)
    price = db.Column(db.Integer, nullable = True)
    date_purchase = db.Column(db.DateTime, nullable = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    type = "object"
    properties = {
        'purchase_id': {
            'type': 'integer',
            'format': 'inte4'
        },
        'purchase_name': {
            'type': 'string'
        },
        'price': {
            'type': 'integer'
        },
        'date_purchase':{
            'type': 'datetime',
            'format': 'hz'
        },
        'user_id':{
            'type': 'integer'
        }
    }
    required = ["purchase_id", "purchase_name", "date_purchase", "user_id"]
        
    def __init__(self, **kwargs):
        self.purchase_id = kwargs.get('purchase_id')
        self.purchase_name = kwargs.get('purchase_name')
        self.price = kwargs.get('price')
        self.date_purchase = kwargs.get('date_purchase')
        self.user_id = kwargs.get('user_id')
    
    db.create_all()
    def __repr__(self):
        return '<id_purchase %r>' % self.purchase_id