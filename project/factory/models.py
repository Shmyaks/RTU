from flask_restful_swagger_3 import Schema

class FactorySHEMA(Schema):
    type = "object"
    properties = {
        'factory_id': {
            'type': 'integer',
            'format': 'int64'
        },
        'factory_name': {
            'type': 'string'
        },
        'product_id': {
            'type': 'integer',
            'format': 'int64'
        },
        'product_storage': {
            'type': 'integer',
            'format': 'inte64'
        },
        'delivery_time': {
            'type': 'Datetime'
        }
    }