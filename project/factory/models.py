
from flask_restful_swagger_3 import Schema

class CategorySHEMA(Schema):
    type = "object"
    properties = {
        'category_id': {
            'type': 'integer',
            'format': 'int64'
        },
        'category_name': {
            'type': 'string'
        }
    }

class Category_listSHEMA(Schema):
    type = "object"
    properties = {
        'categories': CategorySHEMA
    }


class ProductSHEMA(Schema):
    type = "object"
    properties = {
        'product_id': {
            'type': 'integer',
            'format': 'int64'
        },
        'product_name': {
            'type': 'string'
        }
    }


class UsersSHEMA(Schema):
    type = "object"
    properties = {
        'user_id': {
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


class PurchaseSHEMA(Schema):
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
        },
        'user_category': {
            'type': 'integer',
            'format': 'int64'
        },
        'payment': {
            'type': 'String',
            'format': 'Choises'
        },
        'shop_id': {
            'type': 'integer',
            'format': 'int64'
        },
        'check_shop': {
            'type': 'integer'
        },
        'category_shop': {
            'type': 'integer',
            'format': 'int64'
        }
    }
    required = ["purchase_id", "purchase_name", "date_purchase", "user_id"]


class ShopSHEMA(Schema):
    type = "object"
    properties = {
        'shop_id': {
            'type': 'integer',
            'format': 'int64'
        },
        'shop_name': {
            'type': 'string'
        },
        'shop_phone': {
            'type': 'string'
        },
        'isActive': {
            'type': 'boolean'
        }
    }
    required = ["purchase_id", "purchase_name", "date_purchase", "user_id"]


class UserCategorySHEMA(Schema):
    type = "object"
    properties = {
        'user_category_id': {
            'type': 'integer',
            'format': 'int64'
        },
        'user_id':{
            'type': 'integer',
            'format': 'int64'
        },
        'user_category_name':{
            'type': 'string'
        },
    }

class ProductSHEMA(Schema):
    type = "object"
    properties = {
        'product_name': {
            'type': 'string'
        },
        'product_description':{
            'type':'string'
        },
        'product_price': {
            'type': 'int',
            'format': 'int64'
        },
        'shop_name': {
            'type': 'string'
        },
        'category_name': {
            'type': 'string'
        },
        'category_id': {
            'type': 'int',
            'format': 'int64'
        }
    }

class Product_listSHEMA(Schema):
    type = "object"
    properties = {
        'products': ProductSHEMA
    }