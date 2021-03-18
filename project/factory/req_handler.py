#This is request handler.
from flask_restful_swagger_3 import Resource
from flask import jsonify
from flask_restful_swagger_3 import swagger
from flask_restful.reqparse import RequestParser
from database import Factory, Crafting
from __main__ import db, scheduler
from secrets import  token_hex
from somefunc import to_dict, check_storage
from models import FactorySHEMA, MessageSHEMA, crafting_list_itemsSHEMA

@swagger.tags('Factory')
class Factories_routes(Resource):
        
    @swagger.reorder_with(MessageSHEMA, response_code = 200, description='Create factory')
    @swagger.parameter(_in='query', name='factory_name', schema={'type': 'string'}, required=True)
    def post(self):
        post_parser = RequestParser()
        post_parser.add_argument('factory_name', type = str, required = True)
        args = post_parser.parse_args()
        factory = Factory(**args)
        
        db.session.add(factory)
        db.session.commit()

        return jsonify({"message":"Create factory {} successful".format(factory.factory_name)})

    @swagger.reorder_with(FactorySHEMA, response_code = 200, description = "OK")
    @swagger.parameter(_in='query', name='factory_id', schema={'type': 'integer'}, required=True)
    @swagger.reorder_with(MessageSHEMA, response_code=404, description="The factory_id 0 does not exist")
    def get(self):
        post_parser = RequestParser()
        post_parser.add_argument('factory_id', type = int)
        args = post_parser.parse_args()
        factory = Factory.query.filter_by(factory_id = args['factory_id']).first_or_404(description='The factory_id {} does not exist '.format(args['factory_id']))
        
        return jsonify(to_dict(factory, FactorySHEMA))
    
    @swagger.reorder_with(MessageSHEMA, response_code=201, description="OK")
    @swagger.parameter(_in='query', name='factory_id', schema={'type': 'integer'}, required=True)
    @swagger.parameter(_in='query', name='factory_name', schema={'type': 'string'}, required=True)
    @swagger.reorder_with(MessageSHEMA, response_code=404, description="The factory_id 0 does not exist")
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

    @swagger.reorder_with(MessageSHEMA, response_code = 200, description = "OK. !!!Delete with scheduler!!!")
    @swagger.parameter(_in='query', name='factory_id', schema={'type': 'integer'}, required=True)
    @swagger.reorder_with(MessageSHEMA, response_code=404, description="The factory does not exist")
    def delete(self):
        delete_parser = RequestParser()
        delete_parser.add_argument('factory_id')
        args = delete_parser.parse_args()

        factory = Factory.query.filter_by(factory_id = args['factory_id']).first_or_404(description='The factory_id {} does not exist '.format(args['factory_id'])) 

        crafts = factory.crafts.all()
        for craft in crafts:
            scheduler.remove_job(job_id = craft.scheduler_id)

        db.session.commit()

        return jsonify({'message': 'Factory {} was deleted'.format(args['factory_id'])})  

@swagger.tags('Factory craft')
class Craft(Resource): 
    '''Restfull class for Factory craft'''    

    @swagger.reorder_with(MessageSHEMA, response_code=200, description="OK")
    @swagger.reorder_with(MessageSHEMA, response_code=404, description="The factory does not exist")
    @swagger.reorder_with(MessageSHEMA, response_code=409, description="The factory does not exist")
    @swagger.parameter(_in='query', name='interval_delivery', description = "This interval in seconds. Please set SECONDS.", schema={'type': 'integer'}, required=True)
    @swagger.parameter(_in='query', name='craft_count', schema={'type': 'integer'}, required=True)
    @swagger.parameter(_in='query', name='shop_id', schema={'type': 'integer'}, required=True)
    @swagger.parameter(_in='query', name='product_id', schema={'type': 'integer'}, required=True)
    @swagger.parameter(_in='query', name='factory_id', schema={'type': 'integer'}, required=True)
    def post(self):
        '''This add craft product'''

        post_parser = RequestParser()
        post_parser.add_argument('factory_id', type = int, required = True)
        post_parser.add_argument('product_id', type = int, required = True)
        post_parser.add_argument('shop_id', type = int, required = True)
        post_parser.add_argument('craft_count', type = int, required = True)
        post_parser.add_argument('interval_delivery', type = int, required = True)
        args = post_parser.parse_args()

        factory = Factory.query.filter_by(factory_id = args['factory_id']).first_or_404(description='The factory_id {} does not exist '.format(args['factory_id'])) 
        storage = factory.crafts.filter_by(product_id = args['product_id']).first()
        if storage:
            return {'message': 'Product is crafting in factory {}'.format(factory.factory_id)}, 409
        
        args['scheduler_id'] = token_hex(nbytes=16)

        craft = Crafting(**args)
        
        db.session.add(craft)
        db.session.commit()

        scheduler.add_job(check_storage, 'interval', seconds = args['interval_delivery'], id=args['scheduler_id'], args=[args['factory_id'], args['product_id']])

        return jsonify({'message': 'Success craft was add to factory {}'.format(factory.factory_id)})

    @swagger.reorder_with(crafting_list_itemsSHEMA, response_code=200, description="OK")
    @swagger.reorder_with(MessageSHEMA, response_code=404, description="The factory does not exist")
    @swagger.parameter(_in='query', name='factory_id', schema={'type': 'integer'}, required=True)
    def get(self):
        '''Get crafts products by factory_id'''

        get_parser = RequestParser()
        get_parser.add_argument('factory_id', type = int, required = True)
        args = get_parser.parse_args()

        factory = Factory.query.filter_by(factory_id = args['factory_id']).first_or_404(description='The factory_id {} does not exist '.format(args['factory_id'])) 

        return jsonify(to_dict(factory.crafts.all(), crafting_list_itemsSHEMA, many = True))

    @swagger.reorder_with(MessageSHEMA, response_code=200, description="OK")
    @swagger.reorder_with(MessageSHEMA, response_code=404, description="The factory pr craft does not exist")
    @swagger.parameter(_in='query', name='interval_delivery', schema={'type': 'integer'})
    @swagger.parameter(_in='query', name='shop_id', schema={'type': 'integer'})
    @swagger.parameter(_in='query', name='product_id', schema={'type': 'integer'})
    @swagger.parameter(_in='query', name='craft_id', schema={'type': 'integer'}, required=True)
    @swagger.parameter(_in='query', name='factory_id', description = "Filter by factory_id", schema={'type': 'integer'}, required=True)
    def put(self):

        put_parser = RequestParser()
        put_parser.add_argument('factory_id', type = int, required = True)
        put_parser.add_argument('craft_id', type = int, required = True)
        put_parser.add_argument('product_id', type = int)        
        put_parser.add_argument('shop_id', type = int)
        put_parser.add_argument('interval_delivery', type = int)
        args = put_parser.parse_args()

        factory = Factory.query.filter_by(factory_id = args['factory_id']).first_or_404(description='The factory_id {} does not exist '.format(args['factory_id']))   
        craft = factory.crafts.filter_by(craft_id = args['craft_id']).first_or_404(description='The factory_id {} does not exist '.format(args['factory_id']))

        if args['product_id']:
            craft.product_id = args['product_id']
        else:
            args['product_id'] = craft.product_id
        
        if args['shop_id']:  
            craft.shop_id = args['shop_id']
        else:
            args['shop_id'] = craft.shop_id

        if args['interval_delivery']:      
            craft.interval_delivery = args['interval_delivery']  
        else:
            args['interval_delivary'] = craft.interval_delivery

        args['scheduler_id'] = token_hex(nbytes=16)
        scheduler.remove_job(job_id = craft.scheduler_id)
        craft.scheduler_id = args['scheduler_id']
        scheduler.add_job(check_storage, 'interval', seconds = args['interval_delivery'], id=args['scheduler_id'], args=[args['factory_id'], args['product_id']])

        db.session.commit()

        return jsonify({'message': 'craft {} was updated'.format(craft.craft_id)})    
