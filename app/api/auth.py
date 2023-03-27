from flask import Blueprint, request, jsonify, make_response, url_for, current_app
from app.models import User
from app import db, mail, login_manager
from flask_login import login_user, logout_user, current_user
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, BadSignature

auth_bp = Blueprint('auth', __name__)

def generate_session_id(user_id):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(user_id)

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

    send_welcome_email(new_user)

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
    session_id = generate_session_id(user.id)
    response = make_response(jsonify({'user': user.to_dict(), 'message': "You're logged in"}), 200)
    response.set_cookie('session', session_id, secure=True, samesite='None')
    return response


@auth_bp.route('/check_login', methods=['GET'])
def check_login():
    session_id = request.cookies.get('session')
    if session_id:
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        try:
            user_id = serializer.loads(session_id, max_age=3600)
            user = User.query.get(user_id)
            if user:
                return jsonify({'user': user.to_dict()})
        except BadSignature:
            pass

    return jsonify({'user': None})

@auth_bp.route('/logout', methods=['POST'])

def logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({'message': 'Logged out successfully'}), 200
    else:
        return jsonify({'error': 'You are not logged in'}), 401

@auth_bp.route('/reset_password', methods=['POST'])
def reset_password_request():
    print(f'Current user: {current_user}')
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    user = User.query.filter_by(email=email).first()
    print('user: ', user)
    if user:
        send_password_reset_email(user)

    return jsonify({'message': 'If an account with this email exists, a password reset link has been sent.'}), 200

@auth_bp.route('/reset_token/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_reset_token(token)

    if not user:
        return jsonify({'error': 'Invalid or expired token'}), 400

    if request.method == 'POST':
        data = request.get_json()
        password = data.get('password')

        if not password:
            return jsonify({'error': 'Password is required'}), 400

        user.set_password(password)
        db.session.commit()

        return jsonify({'message': 'Password has been updated successfully'}), 200

    return jsonify({'message': 'Please provide the new password in a POST request'}), 200



def send_welcome_email(user):
    msg = Message("Welcome to our JustQ",
                  sender="justq.main@gmail.com",
                  recipients=[user.email])
    msg.body = f"""Hello {user.username},

Thank you for signing up for our Q&A platform! We're excited to have you on board. Be sure to explore the site and engage with the community.

If you have any questions, feel free to reach out to our support team.

Best regards,
The JustQ Team
"""
    mail.send(msg)

def send_password_reset_email(user):
    reset_token = user.get_reset_token()

    # Change the next line to include the base URL of your front-end consumer
    reset_url = f"{current_app.config['FRONT_END_BASE_URL']}/reset-password/{reset_token}"

    msg = Message("Password Reset Request",
                  sender="noreply@yourdomain.com",
                  recipients=[user.email])
    msg.html = f"""Hello {user.username},

To reset your password, please follow the link below:</br>
<a href="{reset_url}">Click here!</a></br>

If you did not request a password reset, please ignore this email. Your password will remain unchanged.

Best regards,
The Q&A Platform Team
"""
    mail.send(msg)