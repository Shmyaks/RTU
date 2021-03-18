#
#  SQLALCHEMY database
#
from __main__ import db

class Crafting(db.Model):
    craft_id = db.Column(db.Integer, primary_key = True, nullable = True)
    factory_id = db.Column(db.Integer, db.ForeignKey('factory.factory_id'), nullable = True)
    product_id = db.Column(db.Integer, nullable = False)
    craft_count = db.Column(db.Integer, default = 0)
    shop_id = db.Column(db.Integer, nullable = True)
    product_storage = db.Column(db.Integer, default = 0)
    interval_delivery = db.Column(db.Integer, nullable = False)
    scheduler_id = db.Column(db.Integer, nullable = False)

    def __init__(self, **kwargs):
        self.factory_id = kwargs.get('factory_id')
        self.product_id = kwargs.get('product_id')
        self.interval_delivery = kwargs.get('interval_delivery')
        self.shop_id = kwargs.get('shop_id')
        self.scheduler_id = kwargs.get('scheduler_id')
        self.craft_count = kwargs.get('craft_count')


class Factory(db.Model):
    factory_id = db.Column(db.Integer, primary_key = True, nullable = True)
    factory_name = db.Column(db.String(32), nullable = True)
    crafts = db.relationship('Crafting', backref = 'Factory', lazy = True)

    def __init__(self, **kwargs):
        self.factory_name = kwargs.get('factory_name')

    def __repr__(self):
        return '<factory_id %r>' % self.factory_id