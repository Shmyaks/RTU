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
    product_name = db.Column(db.String(32))
    price = db.Column(db.Integer, nullable = True)

    def __init__(self, **kwargs):#Add to database
        self.purchase_id = kwargs.get('purchase_id')
        self.price = kwargs.get('price')
        self.product_name = kwargs.get('product_name')


class Purchase(db.Model):#This is database Purchase. Purchase User.
    purchase_id = db.Column(db.Integer, primary_key = True)
    products = db.relationship('Purchase_items', backref = 'Purchase', lazy = 'dynamic')
    full_price = db.Column(db.Integer, nullable = True)
    purchase_name = db.Column(db.String(32))
    date_purchase = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    user_category_id = db.Column(db.Integer, db.ForeignKey('user_category.user_category_id'))
    payment = db.Column(db.String(16))
    check_id_shop = db.Column(db.Integer, default = 0)
    category_shop = db.Column(db.String)
    
    def add_params(self, **kwargs):
        self.__init__(**kwargs)

    def __init__(self, **kwargs):#Add to database
        self.purchase_id = kwargs.get('purchase_id')
        self.shop_id = kwargs.get('shop_id')
        self.purchase_name = kwargs.get('purchase_name')
        self.full_price = kwargs.get('full_price')
        self.user_id = kwargs.get('user_id')
        self.check_id_shop = kwargs.get('check_shop')
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
        self.user_category_name = kwargs.get('user_category_name')

    def __repr__(self):
        return '<user_category_id %r>' % self.user_category_id