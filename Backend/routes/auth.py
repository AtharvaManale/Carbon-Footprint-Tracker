from flask import jsonify, request, Blueprint, session
from Backend.models.models import users
from Backend.extensions import db

auth = Blueprint("auth", __name__)

@auth.route('/signup', methods = ['POST'])
def signup():
    data = request.json

    user = users.query.filter_by(username = data['username']).first()

    if user:
        return jsonify("Username already used!"), 400

    if data['confirm_password'] != data['password']:
        return jsonify("Please enter similar passwords"), 400

    user = users(
        username = data['username'],
        password = users.create_password(data["password"]),
        shop_name = data.get("shop_name"),
        role = data.get("role")
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Registered successfully!"}), 200


@auth.route('/login', methods = ['POST'])
def login():
    data = request.json

    user = users.query.filter_by(username = data.get('username')).first()

    if not user:
        return jsonify({'error': "user doesn't exists"}), 404
    
    if not user.check_password(data.get('password')):
        return jsonify({'error' : "Credentials don't match!"}), 401
    
    session['user_id'] = user.id
    session['user_role'] = user.role

    return jsonify({'message' : 'Logged in successfully!'}),200