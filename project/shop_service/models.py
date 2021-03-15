
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
        'count': {
            'type':'int',
            'format':'int64'
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


class MessageSHEMA(Schema):
    type = "object"
    properties = {
        'message': {
            'type': 'string'
        }
    }
