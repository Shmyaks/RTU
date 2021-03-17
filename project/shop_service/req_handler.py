#This is request handler.
import sys
from datetime import datetime
from operator import pos
from typing import Dict
from flask_restful_swagger_3 import Resource
from flask import jsonify
from flask_restful_swagger_3 import swagger
import requests
from flask_restful.reqparse import RequestParser
from database import Shop, Product, Category, TableCategory, Check
from __main__ import db
from somefunc import to_dict, tuple_to_dict
import sys
sys.path.append('d:\\RTU BACK\\RTU\\project')
from models import ShopSHEMA, Product_listSHEMA, Category_listSHEMA, MessageSHEMA, ExampleSearchProduct, PurchaseSHEMA, ExampleSetProduct, Check_listSHEMA, ExampleSETlistChecks, ExampleSETlistProduct #MODELS Dictionary database



@swagger.tags('Create_shop')
class Create_shop(Resource): #only by admin. Admin can create a shop
    '''Restful class for create_shop'''
    
    @swagger.reorder_with(MessageSHEMA, response_code=200, description="Create success")
    @swagger.parameter(_in='query', name='shop_name', schema={'type': 'string'}, required=True)
    @swagger.parameter(_in='query', name='shop_address', schema={'type': 'string'}, required=True)
    @swagger.parameter(_in='query', name='shop_phone', schema={'type': 'string'}, required=True)
    def post(self):
        '''Create shop'''

        post_parser = RequestParser()#parser on request
        post_parser.add_argument('shop_name', type = str, required = True)
        post_parser.add_argument('shop_address', type = str, required = True)
        post_parser.add_argument('shop_phone', type = str, required = True)
        args = post_parser.parse_args()
        
        shop = Shop(**args)
        db.session.add(shop)
        db.session.commit()
        
        return jsonify({"message":"Create shop {} successful".format(shop.shop_name)})

@swagger.tags('Shop_Resource')
class Shop_routes(Resource):
    '''Restfull class for Shop Resource'''

    @swagger.reorder_with(ShopSHEMA, response_code=200, description='OK')
    @swagger.reorder_with(ShopSHEMA, response_code=404, description='Shop does not exist')
    def get(self, shop_id: int):
        '''Get shop'''

        return jsonify(to_dict(Shop.query.filter_by(shop_id = shop_id).first_or_404(description='The shop_id {} does not exist '.format(shop_id)),ShopSHEMA))
@swagger.tags('Category_Resource')
class CategorySHOP_routes(Resource):
    '''Restfull class for category shop'''

    @swagger.reorder_with(Category_listSHEMA, response_code=200, description="OK")
    @swagger.reorder_with(MessageSHEMA, response_code=404, description="Shop does not exists")
    @swagger.parameter(_in='query', name='shop_id', description = 'Filter by shop_id or give all categories', schema={'type': 'integer'})
    def get(self):#body parser
        '''Get category'''

        get_parser = RequestParser()
        get_parser.add_argument('shop_id', type = int)
        args = get_parser.parse_args()
        filter_shop = (None == None)
        if args['shop_id']:
            shop =  Shop.query.filter_by(shop_id = args['shop_id']).first_or_404(description='The shop_id {} does not exist '.format(args['shop_id']))
            filter_shop = (Shop.shop_id == args['shop_id'])
       
        #return class Category, not tuple!!!  
        result = db.session.query(Category).select_from(TableCategory).join(Shop).join(Category). \
            filter(filter_shop).all()
        
        return jsonify(to_dict(result,Category_listSHEMA, many = True))

    @swagger.reorder_with(MessageSHEMA, response_code=200, description='OK')
    @swagger.reorder_with(MessageSHEMA, response_code=409, description="Category exists in shop")
    @swagger.reorder_with(MessageSHEMA, response_code=404, description="Shop does not exists")
    @swagger.parameter(_in='query', name='shop_id', schema={'type': 'integer'}, required = True)
    @swagger.parameter(_in='query', name='category_name', description = 'add category to shop', schema={'type': 'string'}, required = True)
    def post(self):
        '''Add category to shop'''
        
        post_parser = RequestParser()
        post_parser.add_argument('category_name', type = str, required = True)
        post_parser.add_argument('shop_id', type = int)
        args = post_parser.parse_args()
        shop = Shop.query.filter_by(shop_id = args['shop_id']).first_or_404(description='The shop_id {} does not exist '.format(args['shop_id']))
        category = shop.categories.filter_by(category_name = args['category_name']).first()
        if category:
            return {'message':'This is category is exists'}, 409
        
        category = Category.query.filter_by(category_name = args['category_name']).first()
        if not category:#Create categories if not exist
            category = Category(**args)
        
        shop.categories.append(category)#If the category is found. Add
                
        return jsonify({'message':'Сategory {} was added in {}'.format(args['category_name'], shop.shop_name)})


@swagger.tags('Product_Resource')
class Product_routes(Resource):
    '''Restfull class for Product Resource'''

    @swagger.reorder_with(MessageSHEMA, response_code=200, description='OK')
    @swagger.reorder_with(MessageSHEMA, response_code=404, description="Shop or Category does not exists")
    @swagger.parameter(_in='query', name='product_name', schema={'type': 'string'}, required = True)
    @swagger.parameter(_in='query', name='product_price', schema={'type': 'integer'}, required = True)
    @swagger.parameter(_in='query', name='product_description', schema={'type': 'string'}, required = True)
    @swagger.parameter(_in='query', name='category_id', description = "Add category for product", schema={'type': 'integer'}, required = True)
    @swagger.parameter(_in='query', name='shop_id', description = "Add prodcut to shop", schema={'type': 'integer'}, required = True)
    def post(self):       
        '''Add product to shop'''

        post_parser = RequestParser()#parsing body request
        post_parser.add_argument('product_name', type = str, required = True)
        post_parser.add_argument('product_price', type = str, required = True)
        post_parser.add_argument('product_description', type = str, required = True)
        post_parser.add_argument('category_id', type = int, required = True)
        post_parser.add_argument('shop_id', type = int, required = True)
        args = post_parser.parse_args()

        shop = Shop.query.filter_by(shop_id = args['shop_id']).first_or_404(description='The shop_id {} does not exist '.format(args['shop_id']))
        category = shop.categories.filter_by(category_id = args['category_id']).first_or_404(description='The category_id {} does not exist in shop_id {}'.format(args['category_id'],shop.shop_id))

        product = Product(**args)#create product
        db.session.add(product)#add to database
        db.session.commit()#commits

        return jsonify({"message":"Product {} was added in {}".format(product.product_id, shop.shop_name)})

    @swagger.reorder_with(Product_listSHEMA, response_code=200, description="OK")
    @swagger.reorder_with(MessageSHEMA, response_code=404, description="Shop does not exists")
    @swagger.parameter(_in='query', name='shop_id', description = "Add product to shop", schema={'type': 'integer'}, required = True)
    @swagger.parameter(_in='query', name = 'products_id', description = 'Filter by products_id', schema = ExampleSETlistProduct)
    def get(self):
        get_parser = RequestParser()
        get_parser.add_argument('shop_id', type = int, required = True)
        get_parser.add_argument('products_id', action = 'append', type = int)
        args = get_parser.parse_args()

        filter_products = (None == None)
        if args['products_id']:
            filter_products =  (Product.product_id.in_(args['products_id']))

        shop = Shop.query.filter(shop_id = args['shop_id']).first_or_404(description='The shop_id {} does not exist '.format(args['shop_id']))
        products = shop.products.filter(filter_products).all()

        return jsonify(products, Product_listSHEMA, many = True)


    @swagger.reorder_with(MessageSHEMA, response_code=200, description="OK")
    @swagger.reorder_with(MessageSHEMA, response_code=404, description="Shop or Category or Product does not exists")
    @swagger.parameter(_in='query', name='product_name', description="Change product_name", schema={'type': 'string'})
    @swagger.parameter(_in='query', name='product_price', description = "Change product_price", schema={'type': 'integer'})
    @swagger.parameter(_in='query', name='product_description', description = "Change product_description", schema={'type': 'string'})
    @swagger.parameter(_in='query', name='category_id', description = "Change category_id", schema={'type': 'integer'})
    @swagger.parameter(_in='query', name='product_id', description = "filter product_id", schema={'type': 'integer'}, required = True)
    @swagger.parameter(_in='query', name='shop_id', description = "filter shop_id", schema={'type': 'integer'}, required = True)
    def put(self):
        '''UPDATE product'''

        put_parser = RequestParser()
        put_parser.add_argument('product_id', type = int, required = True)
        put_parser.add_argument('shop_id', type = int, required = True)
        put_parser.add_argument('product_name', type = str)
        put_parser.add_argument('product_price', type = str)
        put_parser.add_argument('product_description', type = str)
        put_parser.add_argument('category_id', type = int)
        args = put_parser.parse_args()
        
        shop = Shop.query.filter_by(shop_id = args['shop_id']).first_or_404(description='The shop_id {} does not exist '.format(args['shop_id']))
        product = shop.products.filter_by(product_id = args['product_id']).first_or_404(description='The product_id {} does not exist in {}'.format(args['product_id'], shop.shop_id))
        if args['category_id']:
            category = shop.categories.filter_by(category_id = args['category_id']).first_or_404(description='The category_id {} does not exist in shop_id {}'.format(args['category_id'], shop.shop_id))
            product.category_id = category.category_id
        if args['product_name']:
            product.product_name = args['product_name']#change
        if args['product_price']:
            product.product_price = args['product_price']#change
        if args['product_description']:
            product.product_description = args['product_description']#change
        
        db.session.add(product)#add to databasse
        db.session.commit()#commit

        return jsonify({"message":"Product {} was updated".format(args['product_id'])})
@swagger.tags('Search_product')
class Shop_product(Resource):

    @swagger.reorder_with(Product_listSHEMA, response_code=200, description='OK')
    @swagger.parameters([{'in': 'query', 'name': 'body', 'description': 'Search product by name. You can set multiple values for filters (shop_id, category_id).', 'schema': ExampleSearchProduct, 'required': 'true'}])
    def get(self):
        '''Get product'''

        get_parser = RequestParser()
        get_parser.add_argument('shop_id', action='append', required = True, type = int)
        get_parser.add_argument('category_id', action='append', required = True, type = int)
        get_parser.add_argument('product_name', type = str)
        args = get_parser.parse_args()

        filter_shop = (None == None)
        filter_category = (None == None)
        filter_product_name = (None == None)
        if args['shop_id']:#if was in body request
            filter_shop = (Shop.shop_id.in_(args['shop_id']))
        if args['category_id']:#if was in body request
            filter_category = (Category.category_id.in_(args['category_id']))
        if args['product_name']:#if was in body request
            filter_product_name = (Product.product_name == args['product_name'])
        
        #JOIN SQL
        result = db.session.query(Product.product_name, Product.product_description, Product.product_price, Shop.shop_name, Category.category_name, Category.category_id).join(Shop).join(Category).filter(filter_shop, filter_category, filter_product_name).all()

        return jsonify(tuple_to_dict(result, Product_listSHEMA, many = True))#convert tuple

@swagger.tags('Buy_products')
class Shop_buy(Resource):
    '''Restfull class shop_buy'''

    @swagger.reorder_with(PurchaseSHEMA, response_code=200, description="OK")
    @swagger.reorder_with(MessageSHEMA, response_code=404, description="Shop or Products or User does not exists")
    @swagger.reorder_with(MessageSHEMA, response_code=503, description="Purchase service does not work")
    @swagger.parameter(_in='query', name='payment', description = "Set payment", schema={'type': 'string','enum': ['Card', 'Cash']})
    @swagger.parameter(_in='query', name='products', description = "products_id. You can set multiple volumes in your requests", schema= ExampleSetProduct, required = True)
    @swagger.parameter(_in='query', name='purchase_name', schema={'type': 'string'})
    @swagger.parameter(_in='query', name='user_id', schema={'type': 'integer'}, required = True)
    @swagger.parameter(_in='query', name='shop_id', schema={'type': 'integer'}, required = True)
    def post(self):
        '''Buy products'''

        post_parser = RequestParser()
        post_parser.add_argument('shop_id', type = int, required = True)
        post_parser.add_argument('products', action = 'append', type = dict, required = True)#USE LIST
        post_parser.add_argument('payment', type=str, choices=['Cash', 'Card'], required = True)
        post_parser.add_argument('purchase_name', type = str)
        post_parser.add_argument('user_id', type = int, required = True)
        args = post_parser.parse_args()
        print(args['products'])

        shop = Shop.query.filter_by(shop_id = args['shop_id']).first_or_404(description='The shop_id {} does not exist '.format(args['shop_id']))#search in database
        sorted_dict = sorted(args['products'], key=lambda k: k['id'])
        list_products_id = [x.get('id') for x in sorted_dict]#For search in database
        print(list_products_id)
        list_products = shop.products.filter(Product.product_id.in_(list_products_id)).all()#Search
        print(list_products)
        args['full_price'] = 0
        if len(list_products_id) != len(list_products):#If body invalid. OR if have similar args
            return {'message':'Invalid request body or product does not exists'}, 404
       
        if not args['purchase_name']: #This purchase_name. If dont set name will be Purchase
            args['purchase_name'] = 'Purchase'#base name purchase
        
        categories = []
        for i in range(0, len(sorted_dict)):
            if sorted_dict[i].get('count') > list_products[i].count:
                return {'message':'Wrong count product'}, 400
           
            list_products[i].count -= sorted_dict[i].get('count') 
            args['full_price'] += list_products[i].product_price * sorted_dict[i].get('count')
            sorted_dict[i]['product_name'] = list_products[i].product_name   
            sorted_dict[i]['price'] = list_products[i].product_price
            categories.append(list_products[i].category_id)

        # #Automatic category from shop
        setarr = set(categories)
        if len(categories) == len(setarr):#if the categories are unique. Set the category different
            args['category_shop'] = 'different' #1 - this category different.
            args['category_id_shop'] = 1
        else:
            args['category_id_shop'] = categories[0]
            args['category_shop'] = categories[0].category_name #If the categories are not unique. 

        check = shop.checks.all()
        print(check)
        if check == []:
            args['check_id_shop'] = 1
        else:
            args['check_id_shop'] = check[-1].check_id_shop + 1
        
        print(args['check_id_shop'])    

        args['products'] = sorted_dict
        
        try:
            result = requests.post('http://127.0.0.1:5001/purchase', json = args)
        except requests.exceptions.ConnectionError:
            return jsonify({'message':'Purchase service does not work'})

        if result.status_code == 404:
            return jsonify({'message':'user_id {} does not exists'.format(args['user_id'])}), 503


        print(result.json())
        check = Check(**result.json())
        
        db.session.add(check)
        db.session.commit()

        return result.json()


@swagger.tags('Checks')
class Checks(Resource):
    '''Restfull class Checks'''

    @swagger.reorder_with(Check_listSHEMA, response_code=200, description='OK')
    @swagger.reorder_with(MessageSHEMA, response_code=404, description='Shop does not exists')
    @swagger.parameter(_in='query', name='shop_id', schema={'type': 'string'}, required = True)
    def get(self):
        '''Get checks'''

        get_parser = RequestParser()
        get_parser.add_argument('shop_id', type = int, required = True)
        args = get_parser.parse_args()
        
        shop = Shop.query.filter_by(shop_id = args['shop_id']).first_or_404(description='The shop_id {} does not exist '.format(args['shop_id']))#search in database
        checks = shop.checks.all()
        
        return jsonify(to_dict(checks, Check_listSHEMA, many=True))

@swagger.tags('Checks')
class Checks_products(Resource):
    '''Restfull class Checks_Product'''

    @swagger.reorder_with(PurchaseSHEMA, response_code=200, description="OK")
    @swagger.reorder_with(MessageSHEMA, response_code=404, description="Shop does not exist")
    @swagger.parameter(_in='query', name='checks_id', description = "This is routes get purchases. Need only by shop", schema = ExampleSETlistChecks, required=True)
    @swagger.parameter(_in='query', name='shop_id', description = "This is routes get purchases from purchases service", schema = {'type': 'integer'}, required=True)
    def get(self):
        '''Get product by check'''

        get_parser = RequestParser()
        get_parser.add_argument('shop_id', type = int, required = True)
        get_parser.add_argument('checks_id', action = 'append', type = int, required = True)
        args = get_parser.parse_args()

        shop = Shop.query.filter_by(shop_id = args['shop_id']).first_or_404(description='The shop_id {} does not exist '.format(args['shop_id']))#search in database
        checks = shop.checks.filter(Shop.shop_id.in_(args['checks_id'])).all()
        args['purchases_id'] = [x.purchase_id for x in checks]

        print(args)
        try:
            result = requests.get('http://127.0.0.1:5001/purchases', json = args)
        except requests.exceptions.ConnectionError:
            return jsonify({'message':'Purchase service does not work'})
        
        return result.json()

@swagger.tags('Delivery')
class Delivery(Resource):

    @swagger.reorder_with(MessageSHEMA, response_code=201, description='OK')
    @swagger.reorder_with(MessageSHEMA, response_code=404, description="Delivary invalid. Example: shop or product does not exist")
    @swagger.parameter(_in='query', name='count', description = "Add count to product", schema = {'type': 'integer'}, required=True)
    @swagger.parameter(_in='query', name='product_id', schema = {'type': 'integer'}, required=True)
    @swagger.parameter(_in='query', name='shop_id', schema = {'type': 'integer'}, required=True)
    def post(self):

        post_parser = RequestParser()
        post_parser.add_argument('product_id', type = int, required = True)
        post_parser.add_argument('shop_id', type = int, required = True)
        post_parser.add_argument('count', type = int, required = True)
        args = post_parser.parse_args()

        shop = Shop.query.filter_by(shop_id = args['shop_id']).first_or_404(description='Delivery invalid '.format(args['shop_id']))#search in database
        product = shop.products.filter_by(product_id = args['product_id']).first_or_404(description='Delivery invalid '.format(args['shop_id']))#

        product.count += args['count']

        db.session.commit()

        return jsonify({'message': "Delivary success"})