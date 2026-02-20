from flask import Flask, jsonify, request, Blueprint
from Backend.models.models import vendors
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token
from sqlalchemy.exc import IntegrityError
from Backend.extensions import db


auth = Blueprint("auth", __name__)

@auth.routes('/signup', methods = ['POST'])
def signup():
    data = request.json

    user = vendors.query.filter_by(username = data['username']).first()
    
    if user:
        return jsonify("Username already used!"), 400

    if data['confirm_password'] != data['password']:
        return jsonify("Please enter similar passwords"), 400

    user = vendors(
        username = data['username'],
        password = user.create_password(data["password"]),
        admin = data.get('admin')
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Registered successfully!"}), 200


@auth.route('/login', methods = ['POST'])
def login():
    data = request.json

    user = vendors.query.filter_by(username = data.get('username')).first()

    if not user:
        return jsonify({'error': "user doesn't exists"}), 404
    
    if not user.check_password(data.get('password')):
        return jsonify({'error' : "Credentials don't match!"}), 402
    
    access_token = create_access_token(identity=user.admin)
    refresh_token = create_refresh_token(identity=user.admin)

    return jsonify({'message' : 'Logged in successfully!'}),200