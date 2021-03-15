#This is request handler.
from datetime import datetime
from flask_restful_swagger_3 import Resource
from flask import jsonify
from flask_restful_swagger_3 import swagger
from flask_restful.reqparse import RequestParser
from database import Factory
from __main__ import db
from models import FactorySHEMA
from secrets import token_hex  #For generation api_key shop and Factory 

def to_dict(database_object, SHEMA, many = False): #Convert Object to SHEMA in Python dict. If need handle list -> use many = True, but !!USE!! the list schema

    def convert_to_dict(database_object, SHEMA):
        dictionary = {}
        for column in database_object.__table__.columns:#Compare by database columns
            if SHEMA.properties.get(column.name):
                dictionary[column.name] = str(getattr(database_object, column.name))#Adding without order
            
        dictionary = {**SHEMA.properties, **dictionary}#Compare and arrange them in the right order
        print(dictionary)
        return dictionary

    if many:
        list_dictionary_converted = []
        name_list = None# First element dict SHEMA (if use many)
        for param in SHEMA.properties:
            name_list = param
        for i in range(0, len(database_object)):#Handle list
            list_dictionary_converted.append(convert_to_dict(database_object[i], SHEMA.properties[name_list]))
        dictionary = {}
        dictionary[name_list] = list_dictionary_converted
        return dictionary

    return convert_to_dict(database_object, SHEMA)

def tuple_to_dict(tuple_object, SHEMA, many = False):#many = True if need handle list, but !!USE!! the list schema

    #Convert tuple to dict. 
    #We arrange them according to the principle of 1 in the tuple, 1 in the SHEMA.properties. 2 in tuple, 2 in SHEMA.properties and etc.
    def convert_to_dict(tuple_object, SHEMA):
        print(SHEMA.properties)
        dictionary = dict(zip(SHEMA.properties, tuple_object))
        
        return dictionary
    
    if many:
        list_dictionary_converted = []
        name_list = None# First element dict SHEMA (if use many)
        for param in SHEMA.properties:
            name_list = param
        for i in range(0, len(tuple_object)):
            list_dictionary_converted.append(convert_to_dict(tuple_object[i], SHEMA.properties[name_list]))
        dictionary = {}
        dictionary[name_list] = list_dictionary_converted
        
        return dictionary
    
    return convert_to_dict(tuple_object, SHEMA)


class Create_Factory(Resource):
    post_parser = RequestParser()
    post_parser.add_argument('factory_name', type = str, required = True)
    post_parser.add_argument('product_id', type = int, required = True)
    
    @swagger.tags('Factory_create')
    @swagger.response(201, description='Create factory')
    @swagger.reqparser(name = 'Response Factory', parser = post_parser)
    def post(self):
        args = self.post_parser.parse_args()
        args['api_key'] = token_hex(nbytes=64)
        factory = Factory(**args)
        
        db.session.add(factory)
        db.session.commit()

        return jsonify({"message":"Create factory {} successful".format(factory.factory_name), "api-key":"{}".format(args['api_key'])})

@swagger.tags('Factory')
class Factories_routes(Resource):
    @swagger.reorder_with(FactorySHEMA, response_code = 200, description = "Return factory")
    @swagger.parameter(_in='query', name='factory_id', description='factory id',schema={'type': 'integer'}, required=True)
    @swagger.response(response_code=404, description="The factory_id 0 does not exist")
    def get(self):
        post_parser = RequestParser()
        post_parser.add_argument('factory_id', type = int, required = True)
        args = post_parser.parse_args()
        factory = Factory.query.filter_by(factory_id = args['factory_id']).first_or_404(description='The factory_id {} does not exist '.format(args['factory_id']))
        
        return jsonify(to_dict(factory, FactorySHEMA))
    
    @swagger.response(response_code=201, description="Return up")#This auto swagger.
    @swagger.parameter(_in='query', name='factory_id', schema={'type': 'integer'}, required=True)
    @swagger.parameter(_in='query', name='factory_name', schema={'type': 'string'}, required=True)
    @swagger.response(response_code=404, description="The factory_id 0 does not exist")
    def put(self):       
        post_parser = RequestParser()
        post_parser.add_argument('factory_id', type = int, required = True)
        post_parser.add_argument('factory_name', type = str, required = True)
        args = post_parser.parse_args()#parse
        factory = Factory.query.filter_by(factory_id = args['factory_id']).first_or_404(description='The factory_id {} does not exist '.format(args['factory_id']))        

        factory.factory_name = args['factory_name']

        db.session.add(factory)
        db.session.commit()

        return jsonify({'message':'factory {}  was updated'.format(factory.factory_id)})

    # def delete(self):
    #     delete_parser = RequestParser()
    #     delete_parser.add_argument('factory_id')