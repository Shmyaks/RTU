#This is request handler.
from datetime import datetime
from flask_restful_swagger_3 import Resource
from flask import jsonify
from flask_restful.reqparse import RequestParser
from database import  Users, Purchase, Shop, Product, Category, User_category, Purchase_items, TableCategory
from models import UsersSHEMA, PurchaseSHEMA, ShopSHEMA, ProductSHEMA, CategorySHEMA, Product_listSHEMA, Category_listSHEMA#MODELS Dictionary database
from __main__ import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from secrets import  token_hex  #For generation api_key shop and Factory 

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

def ApiKey_shop_required(func):#api key shop
    def wrapper(*args, **kwargs):
        header_parser = RequestParser()
        header_parser.add_argument('x-api-key', location='headers', help = "No detecteed Api_key in headers", required = True)
        args = header_parser.parse_args()
        shop = Shop.query.filter_by(api_key = args['x-api-key']).first()
        kwargs['shop'] = shop
        if shop:
            functional = func(*args, **kwargs)
            return functional
        
        return jsonify({'message':'Shop Api key was skipped or invalid'})
    
    return wrapper

class Purchase_routes(Resource):
    # @jwt_required() #Need to jwt token
    # def post(self):
    #     post_parser = RequestParser()
    #     post_parser.add_argument('price', type=str, required=True)
    #     post_parser.add_argument('purchase_name', type=str, help='Id of new group', required = True)
    #     post_parser.add_argument('date_purchase', type=lambda x: datetime.strptime(x,'%Y-%m-%dT%H:%M:%S'), help = 'Datetime purchase', required = True)
    #     args = post_parser.parse_args()
    #     args['user_id'] = get_jwt_identity()
    #     purchase = Purchase(**args)
    #     db.session.add(purchase)
    #     db.session.commit()
        
    #     return jsonify({"message":"Purchase {} was added".format(purchase.purchase_id)})

    @jwt_required() #Need to jwt token
    def get(self):
        get_parser = RequestParser()
        get_parser.add_argument('user_id', required = True)
        args = get_parser.parse_args()
        real_user = Users.query.filter_by(user_id = get_jwt_identity()).first()
        user = Users.query.filter_by(user_id = args['user_id']).first_or_404(description='The user_id {} does not exist '.format(args['user_id']))

        if user.user_id != real_user.user_id and not real_user.admin:
            return jsonify({'message':'You have not got permission'})
        
        list_purchases = []
        for purchase in user.purchases:
            list_purchases.append(to_dict(purchase,PurchaseSHEMA))
            
        return jsonify(list_purchases)

    @jwt_required() #Need to jwt token
    def delete(self):
        get_parser = RequestParser()
        get_parser.add_argument('user_id', type = int ,required = True)
        get_parser.add_argument('purchase_id', type = int, required=True)
        args = get_parser.parse_args()     
        if args['user_id'] != get_jwt_identity() and Users.query.filter_by(admin = True, user_id = get_jwt_identity()).first():
            return jsonify({'message':'You dont have permission'})
        
        user = Users.query.filter_by(user_id = args['user_id']).first_or_404(description='The user_id {} does not exist '.format(args['user_id']))
        purchase = user.purchases.filter_by(purchase_id = args['purchase_id']).first_or_404(description = 'The purchase {} does not exist in user {}'.format(args['purchase_id'],args['user_id']))
        
        db.session.delete(purchase)
        db.session.commit()

        return jsonify({"message":"Purchase {} was deleted".format(args['purchase_id'])})

    @jwt_required()
    def put(self):
        put_parser = RequestParser()
        put_parser.add_argument('user_id', type = int, required = True)
        put_parser.add_argument('purchase_id', type = int, required = True)
        put_parser.add_argument('payment', type = str, choices=['Cash', 'Card'])
        put_parser.add_argument('user_category_id', type = int)
        args = put_parser.parse_args()
 
        if args['user_id'] != get_jwt_identity() and not Users.query.filter_by(admin = True, user_id = get_jwt_identity()):
            return jsonify({'message':'You dont have permission'})
        
        user = Users.query.filter_by(user_id = args['user_id']).first_or_404(description='The user_id {} does not exist '.format(args['user_id']))
        purchase = user.purchases.filter_by(purchase_id = args['purchase_id']).first_or_404(description = 'The purchase {} does not exist in user {}'.format(args['purchase_id'],args['user_id']))

        if args['payment']:
            purchase.payment = args['payment']
        
        if args['user_category_id']:
            user.user_categories.filter_by(user_category_id = args['user_categpry_id']).first_or_404(description = 'The user_category_id {} does not exist in user {}'.format(args['purchase_id'],args['user_id']))
            purchase.user_category_id = args['user_category_id']
        
        db.session.add(purchase)
        db.session.commit()

        return jsonify({'message':'Purchase {} was updated'.format(purchase.purchase_id)})

class User_routes(Resource):
    def get(self,user_id: int):
        return jsonify(to_dict(Users.query.filter_by(user_id = user_id).first_or_404(description='The user_id {} does not exist'.format(user_id)), UsersSHEMA))

    @jwt_required() #Need to jwt token
    def put(self,user_id: int):
        put_parser = RequestParser()
        put_parser.add_argument('first_name', type = str, help = "first_name")
        put_parser.add_argument('second_name', type = str, help = "second_name")
        args = put_parser.parse_args()
        user = Users.query.filter_by(user_id = user_id).first_or_404(description='The user_id {} does not exist'.format(user_id))
        if user.user_id != get_jwt_identity() and not Users.query.filter_by(user_id = get_jwt_identity(), admin = True).first():
            return jsonify({'message':'You dont have permission'})
        
        if args['first_name']:
            user.first_name = args['first_name']
        if args['second_name']:
            user.second_name = args['second_name']
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({"message": "User {} was updated".format(user.login)})


class User_categories_routes(Resource):
    @jwt_required()
    def get(self):
        get_parser = RequestParser()
        get_parser.add_argument('user_id', type = int, required = True)
        args = get_parser.parse_args()
        user = Users.query.filter_by(user_id = args['user_id']).first_or_404(description='The user_id {} does not exist '.format(args['user_id']))
        if args['user_id'] != get_jwt_identity() and not Users.query.filter_by(user_id = get_jwt_identity(), admin = True).first():
            return jsonify({'message':'You dont have permission'})

        list_categories = []
        for category in user.user_categories:
            list_categories.append(to_dict(category, CategorySHEMA)) 
        
        return jsonify(list_categories)
    
    @jwt_required()
    def post(self):
        post_parser = RequestParser()
        post_parser.add_argument('user_id')
        post_parser.add_argument('user_category_name')
        args = post_parser.parse_args()
        user = Users.query.filter_by(user_id = args['user_id']).first_or_404(description='The user_id {} does not exist '.format(args['user_id']))
        if args['user_id'] != get_jwt_identity() and not Users.query.filter_by(user_id = get_jwt_identity(), admin = True).first():
            return jsonify({'message':'You dont have permission'})

        if user.user_categories.filter_by(user_category_name = args['user_category_name']).first():#search category from user
            return jsonify({'message':'This category {} already exists'.format(args['user_category_name'])})

        user_category = User_category(**args)
        db.session.add(user_category)
        db.session.commit()

        return jsonify({'message':'user_category {} was added'.format(user_category.user_category_id)})

    @jwt_required()
    def put(self):
        put_parser = RequestParser()
        put_parser.add_argument('user_id', required = True)
        put_parser.add_argument('user_category_name', required = True)
        put_parser.add_argument('user_category_id', required = True)
        args = put_parser.parse_args()
        user = Users.query.filter_by(user_id = args['user_id']).first_or_404(description='The user_id {} does not exist '.format(args['user_id']))
        category = Users.query.filter_by(user_category_id = args['user_category_id']).first_or_404(description='The user_category_id {} does not exist '.format(args['user_category_id']))

        if category.user_id != get_jwt_identity() or not Users.query.filter_by(admin = True, user_id = get_jwt_identity()):
            return jsonify({'message':'You dont have permission'})

        if user.user_categories.filter_by(user_category_name = args['user_category_name']).first():#search category from user
            return jsonify({'message':'This category {} already exists'.format(args['user_category_name'])})
        
        category.user_category_name = args['user_category_name']
        db.session.add(category)
        db.session.commit()

        return jsonify({'message':'Category {} was updated'.format(category.category_id)})

class User_registration(Resource):
    def post(self):
        post_parser = RequestParser()
        post_parser.add_argument('first_name', type=str, help ="Name", required = True)
        post_parser.add_argument('second_name', type=str, required = True)
        post_parser.add_argument('login', type=str, required = True)
        post_parser.add_argument('password', type=str, required = True)
        args = post_parser.parse_args()
        result = Users.query.filter_by(login=args['login']).first()
        if result:
            return jsonify({"message":"This login is use"})
        
        user = Users(**args)
        db.session.add(user)
        db.session.commit()
       
        return jsonify({"message":"Register is successful"})


class User_login(Resource):
    def post(self):
        post_parser = RequestParser()
        post_parser.add_argument('login', type=str, required = True)
        post_parser.add_argument('password', type=str, required = True)
        args = post_parser.parse_args()
        user = Users.query.filter_by(login = args['login']).first()
        if user is None or not user.check_password(args['password']):
            return jsonify({"message":"Invalid login or password"})
        
        access_token = access_token = create_access_token(identity=user.user_id) #Create_jwt_token and add identity
        
        return jsonify({"message":"Login is successful", "token": access_token})#give token
        

class Admin_Shop(Resource): #only by admin. Admin can create a shop
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = Users.query.filter_by(user_id = user_id).first()
        if user.admin == False:
            return jsonify({"message":"You have not got permissions"})
        
        post_parser = RequestParser()#parser on request
        post_parser.add_argument('shop_name', type = str, required = True)
        post_parser.add_argument('shop_address', type = str, required = True)
        post_parser.add_argument('shop_phone', type = str, required = True)
        args = post_parser.parse_args()
        args['api_key'] = token_hex(nbytes=64)
        shop1 = Shop(**args)
        db.session.add(shop1)
        db.session.commit()
        
        return jsonify({"message":"Create shop {} successful".format(shop1.shop_name),"api-key":"{}".format(args['api_key'])})
    

class Shop_routes(Resource):
    def get(self, shop_id: int):
        shop = Shop.query.filter_by(shop_id = shop_id).first_or_404(description='The shop_id {} does not exist '.format(shop_id))
        
        return jsonify(to_dict(shop,ShopSHEMA))


class CategorySHOP_routes(Resource):
    def get(self):
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

    @ApiKey_shop_required
    def post(self, **kwargs):
        post_parser = RequestParser()
        post_parser.add_argument('category_name', type = str, required = True)
        args = post_parser.parse_args()
        shop = kwargs.get('shop')
        category = shop.categories.filter_by(category_name = args['category_name']).first()
        if category:
            return jsonify({'message':'This is category is use'})
        
        category = Category.query.filter_by(category_name = args['category_name']).first()
        if not category:#Create categories if not exist
            category = Category(**args)
        
        shop.categories.append(category)#If the category is found. Add
        db.session.commit()
                
        return jsonify({'message':'Сategory {} was added in {}'.format(args['category_name'], shop.shop_name)})


class Product_routes(Resource):
    @ApiKey_shop_required
    def post(self, **kwargs):       
        post_parser = RequestParser()
        post_parser.add_argument('product_name', type = str, required = True)
        post_parser.add_argument('product_price', type = str, required = True)
        post_parser.add_argument('product_description', type = str, required = True)
        post_parser.add_argument('category_id', type = int, required = True)
        args = post_parser.parse_args()
        shop = kwargs.get('shop')#from api_key

        category = shop.categories.filter_by(category_id = args['category_id']).first_or_404(description='The category_id {} does not exist in shop_id {}'.format(args['category_id'],shop.shop_id))

        product = Product(**args)
        db.session.add(product)
        db.session.commit()

        return jsonify({"message":"Product {} was added in {}".format(product.product_id, shop.shop_name)})

    def get(self):
        get_parser = RequestParser()
        get_parser.add_argument('shop_id', action='append')
        get_parser.add_argument('category_id', action='append')
        get_parser.add_argument('product_name', type = str)
        args = get_parser.parse_args()
        filter_shop = (None == None)
        filter_category = (None == None)
        filter_product_name = (None == None)
        if args['shop_id']:
            filter_shop = (Shop.shop_id.in_(args['shop_id']))
        if args['category_id']:
            filter_category = (Category.category_id.in_(args['category_id']))
        if args['product_name']:
            filter_product_name = (Product.product_name == args['product_name'])
        
        result = db.session.query(Product.product_name, Product.product_description, Product.product_price, Shop.shop_name, Category.category_name, Category.category_id).join(Shop).join(Category).filter(filter_shop, filter_category, filter_product_name).all()

        return jsonify(tuple_to_dict(result, Product_listSHEMA, many = True))

    
    @ApiKey_shop_required
    def put(self, **kwargs):
        put_parser = RequestParser()
        put_parser.add_argument('product_id', type = int, required = True)
        put_parser.add_argument('product_name', type = str)
        put_parser.add_argument('product_price', type = str)
        put_parser.add_argument('product_description', type = str)
        put_parser.add_argument('category_id', type = int)
        args = put_parser.parse_args()
        
        shop = kwargs.get('shop')#from api_key
        product = shop.products.filter_by(product_id = args['product_id']).first_or_404(description='The product_id {} does not exist in {}'.format(args['product_id'], shop.shop_id))
        if args['category_id']:
            category = shop.categories.filter_by(category_id = args['category_id']).first_or_404(description='The category_id {} does not exist in shop_id {}'.format(args['category_id'], shop.shop_id))
        if args['product_name']:
            product.product_name = args['product_name']
        if args['product_price']:
            product.product_price = args['product_price']
        if args['product_description']:
            product.product_description = args['product_description']
        
        db.session.add(product)
        db.session.commit()

        return jsonify({"message":"Product {} was updated".format(args['product_id'])})
       

class Shop_buy(Resource):
    @jwt_required()
    def post(self):
        post_parser = RequestParser()
        post_parser.add_argument('shop_id', required = True)
        post_parser.add_argument('products_id', action = 'append', required = True)#USE LIST
        post_parser.add_argument('payment', type=str, choices=['Cash', 'Card'], required = True)
        post_parser.add_argument('purchase_name', type = str, reuired = True)
        args = post_parser.parse_args()
        shop = Shop.query.filter_by(shop_id = args['shop_id']).first_or_404(description='The shop_id {} does not exist '.format(args['shop_id']))
        products_list = shop.products.filter(Product.product_id.in_(args['products_id']), Product.count > 0).all()
        args['full_price'] = 0
        args['check_shop'] = shop.check_count
        args['user_id'] = get_jwt_identity()
        if not args['purchase_name']: #This purchase_name. If dont specified will be Purchase
            args['purchase_name'] = 'Purchase'
        
        shop.check_count += 1
        purchase = Purchase()
        categories = []
        for i in range(0,len(args['products_id'])): #handle the products
            product = products_list[int(args['products_id'][i])-1]
            args['full_price'] += product.product_price
            if product.count == 0:#Checking for duplicates
                return jsonify({'message':'Some products are not available in the shop or one of the products in stock'})
            
            product.count -= 1
            categories.append(product.category_id)#Find out what the purchase category will be
            purchase_items = Purchase_items()
            purchase_items.purchase_id = purchase.purchase_id
            purchase_items.product_id = product.product_id
            purchase_items.price = product.product_price
            db.session.add(purchase_items)
            db.session.add(product)
        
        #Automatic category from shop
        setarr = set(categories)
        if len(categories) == len(setarr):#if the categories are unique. Assign the category different
            args['category_shop'] = 1 #1 - this category different. Automatic creation
        else:
            args['category_shop'] = categories[0] #If the categories are not unique. 

        purchase.add_params(**args)
        db.session.add(purchase)
        db.session.commit()

        return jsonify({'message':'Congratulations on your purchase {}'.format(purchase.purchase_id)})

        



