
from flask_restful_swagger_3 import Schema

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

class Purchase_listSHEMA(Schema):
    type = "object"
    properties = {
        'purchases': PurchaseSHEMA.array()
    }


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


class UserCategory_listSHEMA(Schema):
    type = "object"
    properties = {
        'user_categories': UserCategorySHEMA.array()
    }


class MessageSHEMA(Schema):
    type = "object"
    properties = {
        'message': {
            'type': 'string'
        }
    }

class ExamplePurchaseSHEMA(Schema):
    type = "object"
    properties = {
        'user_id': {
            'type': 'integer',
            'format': 'int64'
        },
        'purchase_name': {
            'type': 'string',
            
        },
        'products': productSHEMA.array(),
        'payment': {
            'type': 'string',
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

class ExamplelistPurchase(Schema):
    type = "integer"

class ExampleSETlistPurcase(Schema):
    type = 'object'
    properties = {
        'products_id': ExamplelistPurchase.array()
    }   