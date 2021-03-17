"""Request handler purchase_service."""
from datetime import datetime
from typing import get_args
from flask_restful_swagger_3 import Resource
from flask import jsonify
from flask_restful_swagger_3 import swagger
from flask_restful.reqparse import RequestParser
from database import  Users, User_category, Purchase, Purchase_items
from __main__ import db

import sys
sys.path.append('d:\\RTU BACK\\RTU\\project')
from somefunc import to_dict
from models import UsersSHEMA, PurchaseSHEMA, Purchase_listSHEMA, UserCategory_listSHEMA, MessageSHEMA, ExampleSETlistPurcase#MODELS Dictionary database

@swagger.tags('Purchase_routes')
class Purchase_routes(Resource):
    """Restfull class for purchase"""
    
    @swagger.reorder_with(PurchaseSHEMA, response_code=201,description='OK')
    @swagger.reorder_with(MessageSHEMA, response_code=404,description='User does not exist')
    @swagger.parameters([{'in': 'query', 'name': 'body', 'description': 'Request body', 'schema': PurchaseSHEMA, 'required': 'true'}])
    def post(self):
        """This request need only by Shop."""

        get_parser = RequestParser()
        get_parser.add_argument('shop_id', type = int, required = True)
        get_parser.add_argument('products', action = 'append', type = dict, required = True)#USE LIST
        get_parser.add_argument('payment', type=str, choices=['Cash', 'Card'], required = True)
        get_parser.add_argument('purchase_name', type = str, required = True)
        get_parser.add_argument('user_id', type = int, required = True)
        get_parser.add_argument('check_id_shop', type = int, required = True)
        get_parser.add_argument('full_price', type = int, required = True)
        get_parser.add_argument('category_id_shop', type = int, required = True)
        get_parser.add_argument('category_shop', type = str, required = True)
        args = get_parser.parse_args()        

        Users.query.filter_by(user_id = args['user_id']).first_or_404(description='The user_id {} does not exist '.format(args['user_id']))

        purchase = Purchase(**args)#Create purchasp
        db.session.add(purchase)
        db.session.commit()
        for i in range(0,len(args['products'])): #handle the products
            purchase_item = Purchase_items(**args['products'][i], purchase_id = purchase.purchase_id)#create
            db.session.add(purchase_item)#add purchase_items
        #add purchase to database
        
        db.session.commit()#commit

        return jsonify(to_dict(purchase, PurchaseSHEMA))
    
    @swagger.reorder_with(Purchase_listSHEMA, response_code=200, description='OK')
    @swagger.reorder_with(MessageSHEMA, response_code=404,description='User does not exists')
    @swagger.parameter(_in='query', name='user_id', schema={'type': 'integer'}, required=True)
    def get(self): 
        """Get purchase from user"""

        get_parser = RequestParser()#Parse in body request
        get_parser.add_argument('user_id', required = True)
        args = get_parser.parse_args()
        user = Users.query.filter_by(user_id = args['user_id']).first_or_404(description='The user_id {} does not exist '.format(args['user_id']))#Search in database.

        return jsonify(to_dict(user.purchases.all(), Purchase_listSHEMA, many = True))#Convert

    @swagger.reorder_with(MessageSHEMA, response_code=200, description='Success delete')
    @swagger.reorder_with(MessageSHEMA, response_code=404,description='User, Purchase does not exists')
    @swagger.parameter(_in='query', name='purchase_id', schema={'type': 'integer'}, required=True)
    @swagger.parameter(_in='query', name='user_id', schema={'type': 'integer'}, required=True)
    def delete(self):
        '''Delete purchase from user'''

        get_parser = RequestParser()
        get_parser.add_argument('user_id', type = int ,required = True)#need user_id
        get_parser.add_argument('purchase_id', type = int, required=True)#need purchase_id
        args = get_parser.parse_args()#Parsing body request 
        
        user = Users.query.filter_by(user_id = args['user_id']).first_or_404(description='The user_id {} does not exist '.format(args['user_id']))#search user from bd
        purchase = user.purchases.filter_by(purchase_id = args['purchase_id']).first_or_404(description = 'The purchase {} does not exist in user {}'.format(args['purchase_id'],args['user_id']))#search purchase if user exists
        
        db.session.delete(purchase)#Delete element
        db.session.commit()#COMMIT in database

        return jsonify({"message":"Purchase {} was deleted".format(args['purchase_id'])})

    @swagger.reorder_with(MessageSHEMA, response_code=200,description='OK')
    @swagger.reorder_with(MessageSHEMA, response_code=404,description='User, Purchase, user_category_id does not exists')
    @swagger.parameter(_in='query', name='user_category_id', schema={'type': 'integer'})
    @swagger.parameter(_in='query', name='payment', schema={'type': 'string', 'enum':['Cash', 'Card']})
    @swagger.parameter(_in='query', name='user_id', schema={'type': 'integer'}, required=True)
    @swagger.parameter(_in='query', name='purchase_id', schema={'type': 'integer'}, required=True)
    def put(self):
        """Update purchase from user"""

        put_parser = RequestParser()
        put_parser.add_argument('user_id', type = int, required = True)
        put_parser.add_argument('purchase_id', type = int, required = True)
        put_parser.add_argument('payment', type = str, choices=['Cash', 'Card'])#Cash or Card in body payment
        put_parser.add_argument('user_category_id', type = int)#add user_category_id
        args = put_parser.parse_args()
         
        user = Users.query.filter_by(user_id = args['user_id']).first_or_404(description='The user_id {} does not exist '.format(args['user_id']))#search user in database
        purchase = user.purchases.filter_by(purchase_id = args['purchase_id']).first_or_404(description = 'The purchase {} does not exist in user {}'.format(args['purchase_id'],args['user_id']))

        if args['payment']:
            purchase.payment = args['payment']
        
        if args['user_category_id']:
            user.user_categories.filter_by(user_category_id = args['user_category_id']).first_or_404(description = 'The user_category_id {} does not exist in user {}'.format(args['purchase_id'],args['user_id']))
            purchase.user_category_id = args['user_category_id']
        
        db.session.add(purchase)#add purchase to database
        db.session.commit()#commit

        return jsonify({'message':'Purchase {} was updated'.format(purchase.purchase_id)})

@swagger.tags('Purchase_routes')
class Purchase_get_by_shop(Resource):
    '''Restfull class for get purchase. Only by shop'''
    
    @swagger.reorder_with(Purchase_listSHEMA, response_code=200, description='OK')
    @swagger.parameter(_in='query', name='purchases_id', description = "This is routes get purchases. Need only by shop", schema = ExampleSETlistPurcase, required=True)
    def get(self):
        '''Get purchase'''
        
        get_parser = RequestParser()
        get_parser.add_argument('purchases_id', action = 'append', type = int, required = True)
        args = get_parser.parse_args()

        purchase_list = Purchase.query.filter(Purchase.purchase_id.in_(args['purchases_id'])).all()

        return jsonify(to_dict(purchase_list, Purchase_listSHEMA, many = True))#Many need for list purchases handle

        
@swagger.tags('User_Resource')
class User_routes(Resource):
    """Restful class for user routes"""

    @swagger.reorder_with(UsersSHEMA, response_code=200,description='OK')
    @swagger.reorder_with(MessageSHEMA, response_code=404,description='User does not exists')
    def get(self, user_id: int):
        """Get info user"""
        
        user = Users.query.filter_by(user_id = user_id).first_or_404(description='The user_id {} does not exist'.format(user_id))#search user in database
        
        return jsonify(to_dict(user, UsersSHEMA))#convert by UsersSHEMA

    @swagger.reorder_with(MessageSHEMA, response_code=200, description='Update purchase on user')
    @swagger.reorder_with(MessageSHEMA, response_code=404,description='User does not exists')
    @swagger.parameter(_in='query', name='first_name', schema={'type': 'string'}, required=True)
    @swagger.parameter(_in='query', name='second_name', schema={'type': 'string'}, required=True)
    def put(self,user_id: int):
        """Update info user"""

        put_parser = RequestParser()#parser
        put_parser.add_argument('first_name', type = str, help = "first_name")#parsing arg first_name. Note required
        put_parser.add_argument('second_name', type = str, help = "second_name")#parsing arg second name. Note required
        args = put_parser.parse_args()
        user = Users.query.filter_by(user_id = user_id).first_or_404(description='The user_id {} does not exist'.format(user_id))
        
        if args['first_name']:
            user.first_name = args['first_name']#change first_name
        if args['second_name']:
            user.second_name = args['second_name']#change second_name
        
        db.session.add(user)#add user in database
        db.session.commit()#commit
        
        return jsonify({"message": "User {} was updated".format(user.login)})

@swagger.tags('UserCategory')
class User_categories_routes(Resource):
    """Restfull class for Users category"""

    @swagger.reorder_with(UserCategory_listSHEMA, response_code=200, description='OK')
    @swagger.reorder_with(MessageSHEMA, response_code=404,description='User does not exists')
    @swagger.parameter(_in='query', name='user_id', schema={'type': 'integer'}, required=True)
    def get(self):
        """Get info user categories"""

        get_parser = RequestParser()
        get_parser.add_argument('user_id', type = int, required = True) #need user_id arg in body request
        args = get_parser.parse_args()
        user = Users.query.filter_by(user_id = args['user_id']).first_or_404(description='The user_id {} does not exist '.format(args['user_id'])) #search user in database
        
        return jsonify(to_dict(user.user_categories.all(), UserCategory_listSHEMA, many = True))#convert by UserCategory_listSHEMA. many need for many database objects

    @swagger.reorder_with(MessageSHEMA, response_code=200, description='Add UserCategory')
    @swagger.reorder_with(MessageSHEMA, response_code=404,description='User does not exists')
    @swagger.parameter(_in='query', name='user_category_name', schema={'type': 'string'}, required=True)  
    @swagger.parameter(_in='query', name='user_id', schema={'type': 'integer'}, required=True)   
    def post(self):
        """Add user category"""

        post_parser = RequestParser()
        post_parser.add_argument('user_id', type = int, required = True)
        post_parser.add_argument('user_category_name', type = str, required = True)
        args = post_parser.parse_args()
        
        user = Users.query.filter_by(user_id = args['user_id']).first_or_404(description='The user_id {} does not exist '.format(args['user_id']))#search user in database
        if user.user_categories.filter_by(user_category_name = args['user_category_name']).first():#if user exist check user categories
            return jsonify({'message':'This category {} already exists'.format(args['user_category_name'])})

        user_category = User_category(**args)#create user_category
        db.session.add(user_category)#add to database
        db.session.commit()#commit

        return jsonify({'message':'user_category {} was create'.format(user_category.user_category_id)})

    @swagger.reorder_with(MessageSHEMA, response_code=200,description='OK')
    @swagger.reorder_with(MessageSHEMA, response_code=404,description='User or User_Category does not exists')
    @swagger.reorder_with(MessageSHEMA, response_code=409,description='Exists user_category with user_category name')
    @swagger.parameter(_in='query', name='user_category_name', schema={'type': 'string'}, required=True) 
    @swagger.parameter(_in='query', name='user_category_id', schema={'type': 'integer'}, required=True)
    @swagger.parameter(_in='query', name='user_id', schema={'type': 'integer'}, required=True)
    def put(self):
        """Update user category"""

        put_parser = RequestParser()#parser argsu
        put_parser.add_argument('user_id', required = True)#Need user_id
        put_parser.add_argument('user_category_name', required = True)#Change name
        put_parser.add_argument('user_category_id', required = True)#Need user_category_id
        args = put_parser.parse_args()

        user = Users.query.filter_by(user_id = args['user_id']).first_or_404(description='The user_id {} does not exist '.format(args['user_id']))#search user in database
        category = user.user_categories.filter_by(user_category_id = args['user_category_id']).first_or_404(description='The user_category_id {} does not exist in user {} '.format(args['user_category_id'], args['user_id']))#search user category
        if user.user_categories.filter_by(user_category_name = args['user_category_name']).first():#search similar category
            return {'message':'This category {} already exists'.format(args['user_category_name'])}, 409
        
        category.user_category_name = args['user_category_name'] #change category_name
        db.session.add(category)#add
        db.session.commit()#commit

        return jsonify({'message':'Category {} was updated'.format(category.user_category_id)})


@swagger.tags('UserRegister')
class User_registration(Resource):#user_registr
    """Resftull class register"""

    @swagger.reorder_with(MessageSHEMA, response_code=409,description='Login already exists')
    @swagger.reorder_with(MessageSHEMA, response_code=200,description='Success Register')
    @swagger.parameter(_in='query', name='first_name', schema={'type': 'string'}, required=True)
    @swagger.parameter(_in='query', name='second_name', schema={'type': 'string'}, required=True) 
    @swagger.parameter(_in='query', name='password', schema={'type': 'string'}, required=True)
    @swagger.parameter(_in='query', name='login', schema={'type': 'string'}, required=True)
    def post(self):
        """Register user"""

        post_parser = RequestParser()#Bodyrequest parser
        post_parser.add_argument('first_name', type=str, help ="Name", required = True)#Need first_name
        post_parser.add_argument('second_name', type=str, required = True)#Need second_name
        post_parser.add_argument('login', type=str, required = True)
        post_parser.add_argument('password', type=str, required = True)
        args = post_parser.parse_args()
        result = Users.query.filter_by(login=args['login']).first()
        if result:
            return {"message":"This login is use"}, 409
        
        user = Users(**args)#Create user
        db.session.add(user)#Add to database
        db.session.commit()#Commit
       
        return jsonify({"message":"Register is successful"})


