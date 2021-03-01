from datetime import datetime
from flask_restful_swagger_3 import Resource
from flask import jsonify
from flask_restful.reqparse import RequestParser
from database import  Users, Purchase
from __main__ import db
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

def to_dict(database_model):
    dictionary = {}
    for column in database_model.__table__.columns:
        if database_model.properties.get(column.name):
            dictionary[column.name] = str(getattr(database_model, column.name))
    
    dictionary = {**database_model.properties, **dictionary}

    return dictionary


class routes_purchase(Resource):

    def patch(self):
        ... 
    
    def delete(self, purchase_id: int):
        purchase = Purchase.query.filter_by(purchase_id = purchase_id).first()
        db.session.delete(purchase)
        db.session.commit()

        return jsonify({"message":"Purchase {} was deleted".format(purchase_id)})
        

class add_purchase(Resource):
    @jwt_required()
    def post(self):
        post_parser = RequestParser()
        post_parser.add_argument('price', type=str, required=True)
        post_parser.add_argument('purchase_name', type=str, help='Id of new group', required = True)
        post_parser.add_argument('date_purchase', type=lambda x: datetime.strptime(x,'%Y-%m-%dT%H:%M:%S'), help = 'Datetime purchase', required = True)
        args = post_parser.parse_args()
        args['user_id'] = get_jwt_identity()
        purchase = Purchase(**args)
        db.session.add(purchase)
        db.session.commit()
        
        return jsonify({"message":"Purchase {} was added".format(purchase.purchase_id)})

    @jwt_required()
    def get(self):
        result = Purchase.query.filter_by(user_id = get_jwt_identity()).all()
        for i in range(0, len(result)):
            result[i] = to_dict(result[i])

        return jsonify(result)


class User_routes(Resource):
    @jwt_required()
    def get(self,user_id: int):
        current_user = get_jwt_identity()
        if current_user != user_id:
            return {"permission":"You dont have"}

        return jsonify(to_dict(Users.query.get(current_user)))

    @jwt_required()
    def put(self,user_id: int):
        put_parser = RequestParser()
        put_parser.add_argument('first_name', type = str, help = "first_name")
        put_parser.add_argument('second_name', type = str, help = "second_name")
        args = put_parser.parse_args()
        user = Users.query.get_or_404(user_id)
        if args['first_name']:
            user.first_name = args['first_name']
        if args['second_name']:
            user.second_name = args['second_name']
        db.session.add(user)
        db.session.commit()
        
        return jsonify({"message": "User {} was updated".format(user.login)})


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
            return {"invalid":"Login or password"}
        access_token = access_token = create_access_token(identity=user.id)
        
        return jsonify({"message":"Login is successful", "token": access_token})
        