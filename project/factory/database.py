#
#  SQLALCHEMY database
#
from __main__ import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Users(db.Model):#This is database Users
    user_id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(32), nullable = True)
    second_name = db.Column(db.String(32), nullable = True)
    login = db.Column(db.String(32), nullable = True)
    password = db.Column(db.String())
    date_registration = db.Column(db.DateTime, default = datetime.utcnow)
    admin = db.Column(db.Boolean, default = False)#Big father. For safety
    purchases = db.relationship('Purchase', backref = 'User', lazy='dynamic')
    user_categories = db.relationship('User_category', backref = 'User', lazy = 'dynamic')

    def check_password(self, password: str):#This is method check password 
        return check_password_hash(self.password, password)

    def __init__(self, **kwargs):#Add to database
        self.id = kwargs.get('id')
        self.first_name = kwargs.get('first_name')
        self.second_name = kwargs.get('second_name')
        self.login = kwargs.get('login')
        self.password = generate_password_hash(kwargs.get('password'), method='sha256')#geneerate hash.
        
    def __repr__(self):
        return '<user_id %r>' % self.user_id
    

class Purchase_items(db.Model):#items purchase
    item_id = db.Column(db.Integer, primary_key = True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.purchase_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    price = db.Column(db.Integer, nullable = True)

    def __init__(self, **kwargs):#Add to database
        self.purchase_id = kwargs.get('purchase_id')
        self.product_id = kwargs.get('product_id')
        self.price = kwargs.get('price')


class Purchase(db.Model):#This is database Purchase. Purchase User.
    purchase_id = db.Column(db.Integer, primary_key = True)
    items = db.relationship('Purchase_items', backref = 'Purchase', lazy = 'dynamic')
    full_price = db.Column(db.Integer, nullable = True)
    purchase_name = db.Column(db.String(32))
    date_purchase = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    user_category_id = db.Column(db.Integer, db.ForeignKey('user_category.user_category_id'))
    payment = db.Column(db.String(16))
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.shop_id'))
    check_shop = db.Column(db.Integer, default = 0)
    category_shop = db.Column(db.Integer, db.ForeignKey('category.category_id'))
    
    def add_params(self, **kwargs):
        self.__init__(**kwargs)

    def __init__(self, **kwargs):#Add to database
        self.purchase_id = kwargs.get('purchase_id')
        self.shop_id = kwargs.get('shop_id')
        self.purchase_name = kwargs.get('purchase_name')
        self.full_price = kwargs.get('full_price')
        self.user_id = kwargs.get('user_id')
        self.check_shop = kwargs.get('check_shop') + 1
        self.user_category = kwargs.get('user_category')
        self.category_shop = kwargs.get('category_shop')
        self.payment = kwargs.get('payment')
        
    def __repr__(self):
        return '<id_purchase %r>' % self.purchase_id


class User_category(db.Model):
    user_category_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    user_category_name = db.Column(db.String(32))
    purchases = db.relationship('Purchase', backref = 'User_category', lazy = 'dynamic')

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.user_category_name = kwargs.get('user_id')

    def __repr__(self):
        return '<user_category_id %r>' % self.user_category_id

    
TableCategory = db.Table('TableCategory',
    db.Column('shop_id', db.Integer, db.ForeignKey('shop.shop_id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.category_id'))
)


class Shop(db.Model):
    shop_id = db.Column(db.Integer, primary_key = True)
    shop_name = db.Column(db.String(64), nullable = True)
    shop_phone = db.Column(db.String(16), nullable = True)
    shop_address = db.Column(db.String(100), nullable = True)
    isActive = db.Column(db.Boolean, default = True)
    check_count = db.Column(db.Integer, default = 0)
    api_key = db.Column(db.String(256))
    purchases = db.relationship('Purchase', backref = 'Shop', lazy = 'dynamic')
    categories = db.relationship('Category', secondary=TableCategory, backref='Shops', lazy ='dynamic')
    products = db.relationship('Product', backref = 'Shop', lazy = 'dynamic') 

    def __init__(self, **kwargs):
        self.shop_name = kwargs.get('shop_name')
        self.shop_phone = kwargs.get('shop_phone')
        self.shop_address = kwargs.get('shop_address')
        self.api_key = kwargs.get('api_key')#Generate api key

    def __repr__(self):
        return '<shop_id %r>' % self.shop_id


class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key = True)
    category_name = db.Column(db.String(32), nullable = True)
    products = db.relationship('Product', backref = 'Category', lazy = 'dynamic')
    purchases = db.relationship('Purchase', backref = 'Category', lazy = 'dynamic')

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
    sales = db.relationship('Purchase_items', backref = 'Product', lazy = 'dynamic')
    
    def __init__(self, **kwargs):
        self.product_name = kwargs.get('product_name')
        self.store_id = kwargs.get('shop_id')
        self.category_id = kwargs.get('category_id')
        self.product_price = kwargs.get('product_price')
        self.product_description = kwargs.get('product_description')
        
    def __repr__(self):
        return '<product_id %r>' % self.product_id


class Factory(db.Model):
    factory_id = db.Column(db.Integer, primary_key = True)
    factory_name = db.Column(db.String(32), primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    delivery_time = db.Column(db.DateTime)
    last_delivery_time = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        self.product_id = kwargs.get('product_id')
        self.factory_name = kwargs.get('factory_name')

    def __repr__(self):
        return '<factory_id %r>' % self.factory_id