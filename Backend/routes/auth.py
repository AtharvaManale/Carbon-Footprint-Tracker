from flask import jsonify, request, Blueprint, session
from Backend.models.models import users
from Backend.extensions import db
from datetime import datetime

auth = Blueprint("auth", __name__)

@auth.route('/auditors', methods = ['GET'])
def get_auditors():
    auditors = users.query.filter_by(role = "auditor").all()
    return jsonify({"auditors": [{"auditor_id":auditor.id, "auditor_name":auditor.username}for auditor in auditors]}), 200

@auth.route('/signup', methods=['POST'])
def signup():
    data = request.json

    user = users.query.filter_by(username=data['user_name']).first()
    if user:
        return jsonify({"error": "Username already used!"}), 400

    if data['confirm_password'] != data['password']:
        return jsonify({"error": "Passwords do not match"}), 400

    role = data.get("role")
    auditor_id = None
    end_date = None

    if role != "auditor":

        if not data.get("auditor_id"):
            return jsonify({"error": "Auditor is required"}), 400

        auditor = users.query.get(data["auditor_id"])
        if not auditor or auditor.role != "auditor":
            return jsonify({"error": "Invalid auditor"}), 400

        auditor_id = auditor.id

        if data.get("end"):
            end_date = datetime.strptime(data["end"], "%d-%m-%Y")

    user = users(
        username=data["user_name"],
        role=role,
        shop_name=data.get("shop_name") if role != "auditor" else None,
        auditor_id=auditor_id,
        ending_at=end_date
    )

    user.create_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Registered successfully!"}), 201

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

    return jsonify({
        'message': 'Logged in successfully!',
        'user': {
            'id': user.id,
            'username': user.username,
            'shop_name': user.shop_name,
            'role': user.role,
            'ending_at': user.ending_at.isoformat() if user.ending_at else None
        }
    }), 200

@auth.route('/logout', methods = ['GET', 'POST'])
def logout():
    if "user_id" in session:
        session.clear()
        return jsonify({"message":"Logged out successfully!"}), 200
    return jsonify({"error":"Not logged in!"}), 403

@auth.route('/check', methods = ['GET'])
def check_auth():
    if "user_id" in session:
        user = users.query.get(session["user_id"])
        if user:
            return jsonify({
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "shop_name": user.shop_name,
                    "role": user.role,
                    "ending_at": user.ending_at.isoformat() if user.ending_at else None
                }
            }), 200
    return jsonify({"user": None}), 401