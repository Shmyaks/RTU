
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


class ProductFullSHEMA(Schema):
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
        'products': ProductFullSHEMA.array()
    }


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


class productSMALLSHEMA(Schema):
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


class ExampleSETproduct(Schema):
    type = "integer"


class ExampleSETlistProduct(Schema):
    type = 'object'
    properties = {
        'products_id': ExampleSETproduct.array()
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
        'products': productSMALLSHEMA.array(),
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
        'check_id_shop': {
            'type': 'integer'
        },
        'category_shop': {
            'type': 'string'
        },
        'category_id_shop': {
            'type': 'integer',
            'format': 'int64'
        },
        'shop_id': {
            'type': 'integer',
            'format': 'int64'
        }
    }

    required = [x for x in properties]


class crafting_itemSHEMA(Schema):
    type = "object"
    properties = {
        'craft_id': {
            'type': 'integer',
            'format': 'int64'
        },
        'factory_id': {
            'type': 'integer',
            'format': 'int64'
        },
        'product_id': {
            'type': 'integer',
            'format': 'int64'
        },
        'product_storage': {
            'type': 'integer',
            'format': 'int64'
        },
        'interval_delivery': {
            'type': 'integer',
            'format': 'int64'
        }
    }


class crafting_list_itemsSHEMA(Schema):
    type = "object"
    properties = {
        'crafting_items': crafting_itemSHEMA.array()
    }

class FactorySHEMA(Schema):
    type = "object"
    properties = {
        'factory_id': {
            'type': 'integer',
            'format': 'int64'
        },
        'factory_name': {
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


class product_purchaseSHEMA(Schema):
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
        'products': productSMALLSHEMA.array(),
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


class MessageSHEMA(Schema):
    type = "object"
    properties = {
        'message': {
            'type': 'string'
        }
    }    