from flask import jsonify, request, Blueprint, session
from Backend.models.models import users
from Backend.extensions import db
from datetime import datetime

auth = Blueprint("auth", __name__)

@auth.route('/signup', methods = ['POST'])
def signup():
    data = request.json

    user = users.query.filter_by(username = data['user_name']).first()

    if user:
        return jsonify("Username already used!"), 400

    if data['confirm_password'] != data['password']:
        return jsonify("Please enter similar passwords"), 400

    role = data.get("role")

    end_date = None
    if role != "auditor" and data.get("end"):
        end_date = datetime.strptime(data["end"], "%d-%m-%Y")

    user = users(
        username=data["user_name"],
        role=role,
        shop_name=data.get("shop_name") if role != "auditor" else None,
        ending_at=end_date
    )

    user.create_password(data["password"])
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Registered successfully!"}), 200

@auth.route('/login', methods = ['POST'])
def login():
    data = request.json

    user = users.query.filter_by(username = data.get('user_name')).first()

    if not user:
        return jsonify({'error': "user doesn't exists"}), 404
    
    if not user.check_password(data.get('password')):
        return jsonify({'error' : "Credentials don't match!"}), 401
    
    session['user_id'] = user.id
    session['user_role'] = user.role

    return jsonify({'message' : 'Logged in successfully!'}),200

@auth.route('/logout', methods = ['GET', 'POST'])
def logout():
    if "user_id" in session:
        session.clear()
        return jsonify({"message":"Logged out successfully!"}), 200
    return jsonify({"error":"Not logged in!"}), 403