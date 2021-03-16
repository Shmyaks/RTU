#
#  SQLALCHEMY database
#
from sqlalchemy.orm import backref
from __main__ import db

    
TableCategory = db.Table('TableCategory',
    db.Column('shop_id', db.Integer, db.ForeignKey('shop.shop_id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.category_id'))
)

class Shop(db.Model):
    shop_id = db.Column(db.Integer, primary_key = True)
    shop_name = db.Column(db.String(64), nullable = True)
    shop_phone = db.Column(db.String(16), nullable = True)
    shop_address = db.Column(db.String(100), nullable = True)
    checks = db.relationship('Check', backref = 'Shop', lazy = 'dynamic')
    categories = db.relationship('Category', secondary=TableCategory, backref='Shops', lazy ='dynamic')
    products = db.relationship('Product', backref = 'Shop', lazy = 'dynamic') 

    def __init__(self, **kwargs):
        self.shop_name = kwargs.get('shop_name')
        self.shop_phone = kwargs.get('shop_phone')
        self.shop_address = kwargs.get('shop_address')

    def __repr__(self):
        return '<shop_id %r>' % self.shop_id

class Check(db.Model):
    check_id_database = db.Column(db.Integer, primary_key = True) #This check id in global system database
    check_id_shop = db.Column(db.Integer) #This check id shop
    purchase_id = db.Column(db.Integer) #This id purchase
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.shop_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))
    date_purchase = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        self.check_id_shop = kwargs.get('check_id_shop')
        self.purchase_id = kwargs.get('purchase_id')
        self.shop_id = kwargs.get('shop_id')
        self.category_id = kwargs.get('category_id')
        self.date_purchase = kwargs.get('date_purchase')

    def __repr__(self):
        return '<check_id %r>' % self.check_id_database

class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key = True)
    category_name = db.Column(db.String(32), nullable = True)
    products = db.relationship('Product', backref = 'Category', lazy = 'dynamic')
    checks = db.relationship('Check', backref = 'Category', lazy = 'dynamic')

    def __init__(self, **kwargs):
        self.category_name = kwargs.get('category_name')

    def __repr__(self):
        return '<category_id %r>' % self.category_id


class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key = True)
    product_name = db.Column(db.String(32), nullable = True)
    store_id = db.Column(db.Integer, db.ForeignKey('shop.shop_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))
    product_price = db.Column(db.Integer, nullable = True)
    count = db.Column(db.Integer,  default = 0)
    product_description = db.Column(db.String(256), nullable = True)
    
    def __init__(self, **kwargs):
        self.product_name = kwargs.get('product_name')
        self.store_id = kwargs.get('shop_id')
        self.category_id = kwargs.get('category_id')
        self.product_price = kwargs.get('product_price')
        self.product_description = kwargs.get('product_description')
        
    def __repr__(self):
        return '<product_id %r>' % self.product_id