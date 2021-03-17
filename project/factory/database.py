#
#  SQLALCHEMY database
#
from __main__ import db

class Factory(db.Model):
    factory_id = db.Column(db.Integer, primary_key = True)
    factory_name = db.Column(db.String(32), nullable = False)
    crafting_items = db.relationship('Crafting_items', backref = 'Factory', lazy = 'dynamic')

    def __init__(self, **kwargs):
        self.factory_name = kwargs.get('factory_name')

    def __repr__(self):
        return '<factory_id %r>' % self.factory_id

class Crafting_items(db.Model):
    craft_id = db.Column(db.Integer, primary_key = True)
    factory_id = db.Column(db.Integer, db.ForeignKey('factory.factory_id'))
    product_id = db.Column(db.Integer, nullable = False)
    craft_count = db.Column(db.Integer, default = 0)
    shop_id = db.Column(db.Integer)
    product_storage = db.Column(db.Integer, default = 0)
    interval_delivery = db.Column(db.Integer, nullable = False)
    scheduler_id = db.Column(db.Integer)

    def __init__(self, **kwargs):
        self.factory_id = kwargs.get('factory_id')
        self.product_id = kwargs.get('product_id')
        self.interval_delivery = kwargs.get('interval_delivery')
        self.shop_id = kwargs.get('shop_id')
        self.scheduler_id = kwargs.get('scheduler_id')
        self.craft_count = kwargs.get('craft_count')