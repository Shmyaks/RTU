#
#  SQLALCHEMY database
#
from __main__ import db

class Factory(db.Model):
    factory_id = db.Column(db.Integer, primary_key = True)
    factory_name = db.Column(db.String(32), primary_key = True)
    product_id = db.Column(db.Integer)
    product_storage = db.Column(db.Integer, default = 0)
    delivery_time = db.Column(db.DateTime)
    last_delivery_time = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        self.product_id = kwargs.get('product_id')
        self.factory_name = kwargs.get('factory_name')

    def __repr__(self):
        return '<factory_id %r>' % self.factory_id