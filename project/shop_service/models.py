
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
        'categories': CategorySHEMA.array()
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

    required = [x for x in properties]

class Product_listSHEMA(Schema):
    type = "object"
    properties = {
        'products': ProductSHEMA.array()
    }


class MessageSHEMA(Schema):
    type = "object"
    properties = {
        'message': {
            'type': 'string'
        }
    }

    required = ['message']

class Search_shop_id(Schema):
    type = "integer"


class Search_category_id(Schema):
    type = "integer"
    
class ExampleSearchProduct(Schema):
    type = "object"
    properties = {
        'product_name': {
            'type': 'string'
        },
        'category_id': Search_category_id.array(),
        'shop_id': Search_shop_id.array()
    }

    required = ['shop_id']


class productSHEMA(Schema):
    type = "object"
    properties = {
        'product_name': {
            'type': 'string'
        },
        'price': {
            'type': 'integer',
            'format': 'int64'
        },
        'purchase_id': {
            'type': 'integer',
            'format': 'int64'
        }
    }

    required = [x for x in properties]

class PurchaseSHEMA(Schema):
    type = "object"
    properties = {
        'purchase_id': {
            'type': 'integer',
            'format': 'int64'
        },
        'purchase_name': {
            'type': 'string'
        },
        'full_price': {
            'type': 'integer'
        },
        'date_purchase':{
            'type': 'datetime',
            'format': 'hz'
        },
        'products': productSHEMA.array(),
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
        'check_id_shop': {
            'type': 'integer'
        },
        'category_shop': {
            'type': 'string'
        }
    }

    required = [x for x in properties]


class ExampleSetProduct(Schema):
    type = 'object'
    properties = {
        'id': {
            'type': 'integer',
            'format': 'int64'
        },
        'count': {
            'type': 'integer',
            'format': 'inte64'
        }
    }

    required = ['id', 'count']

class ExampleBuyProducts(Schema):
    type = 'object'
    properties = {
        "user_id": {
            "type": "integer",
            "format": "int64"
        },
        "shop_id": {
            "type": "integer",
            "format": "int64"
        },
        "purchase_name": {
            "type": "string"
        },
        "products": ExampleSetProduct.array(),
        "payment": {
            "type": "string",
            "enum": ['Cash', 'Card']
        }
    }

    required = ['user_id', 'shop_id', 'products', 'payment']


class CheckSHEMA(Schema):
    type = 'object'
    properties = {
        'check_id_database': {
            'type': 'integer',
            'format': 'int64'
        },
        'check_id_shop': {
            'type': 'integer',
            'format': 'int64'
        },
        'purchase_id': {
            'type': 'integer',
            'format': 'int64'
        },
        'shop_id': {
            'type': 'integer',
            'format': 'int64'
        },
        'category_id': {
            'type': 'integer',
            'format': 'int64'
        }
    }

    required = [x for x in properties]

class Check_listSHEMA(Schema):
    type = 'object'
    properties = {
        'checks': CheckSHEMA.array()
    }
class ExamplelistChecks(Schema):
    type = 'integer'


class ExampleSETlistChecks(Schema):
    type = 'object'
    properties = {
        'checks_id': ExamplelistChecks.array()
    }