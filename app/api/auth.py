from flask import Blueprint, request, jsonify, make_response
from flask_login import login_user, logout_user, current_user
from app.models import User
from app import db
from app import login_manager

auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()

    if user:
        return jsonify({'error': 'Email already exists'}), 400

    user = User.query.filter_by(username=username).first()

    if user:
        return jsonify({'error': 'Username already exists'}), 400

    new_user = User(email=email, username=username)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401

    login_user(user, remember='True')
    response = make_response(jsonify({'user': user.to_dict(), 'message': 'Logged in successfully'}), 200)
    # Set the session cookie here
    response.set_cookie("session", "session_value") # Replace "session_value" with the actual session value
    return response

@auth_bp.route('/check_login', methods=['GET'])
def check_login():
    print(current_user)
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.id).first()

        return jsonify({'user': current_user.to_dict()})
    else:
        return jsonify({'user': None})

@auth_bp.route('/logout', methods=['POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({'message': 'Logged out successfully'}), 200
    else:
        return jsonify({'error': 'You are not logged in'}), 401

@auth_bp.route('/reset_password', methods=['POST'])
def reset_password():
    # Implement password reset logic here
    pass