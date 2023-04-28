"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

api = Blueprint('api', __name__)


@api.route('/login', methods = ['POST'])
def login():
    body =request.get_json()
    login=User.query.filter_by(email=body["email"]).first()
    if login:
        token=create_access_token(identity=login.serialize())
        return jsonify(token)
    else:
        return jsonify({"msg":"user not found","status":404,"tu":"pringao"}),404

@api.route('/signup', methods = ['POST'])
def signup():
    body = request.get_json()
    new_user = User(body["email"], body["password"], True)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()),201


@api.route('/user/<int:id>', methods = ['GET'])
def get_user_by_id(id):
    user=User.query.get(id)

    return jsonify(user.serialize()),200

@api.route('/user', methods = ['GET'])
def get_users():            
    all_users=User.query.all()  
    all_users=list(map(lambda user:user.serialize(),all_users)) 

    return jsonify(all_users),200

@api.route('/user/delete', methods = ['POST'])
def delete_user(id):
    user=User.query.get(id).first()
    db.session.remove(user)
    db.session.commit()
    return jsonify(user.serialize()),201
