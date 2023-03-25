from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    questions = db.relationship('Question', backref='author', lazy='dynamic')
    answers = db.relationship('Answer', backref='author', lazy='dynamic')   
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username
        }
    
    def get_reset_token(self, expires_sec=1800):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, max_age=1800):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=max_age)
            user_id = data['user_id']
        except Exception as e:
            return None
        return User.query.get(user_id)



class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=True)
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'), nullable=True)
    vote_type = db.Column(db.String(10), nullable=False)  # 'upvote' or 'downvote'
    timestamp = db.Column(db.DateTime, index=True)

    user = db.relationship('User', backref=db.backref('votes', lazy='dynamic'))


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    votes = db.relationship('Vote', backref='question', lazy='dynamic')
    author = db.relationship('User', backref=db.backref('questions', lazy='dynamic'))
    # ...

    votes = db.relationship('Vote', backref='question', lazy='dynamic')

    def get_votes(self):
        upvotes = Vote.query.filter_by(question_id=self.id, vote_type='upvote').count()
        downvotes = Vote.query.filter_by(question_id=self.id, vote_type='downvote').count()
        return upvotes - downvotes
        
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    author = db.relationship('User', backref=db.backref('answers', lazy='dynamic'))
    votes = db.relationship('Vote', backref='answer', lazy='dynamic')
    
    def get_votes(self):
        upvotes = Vote.query.filter_by(answer_id=self.id, vote_type='upvote').count()
        downvotes = Vote.query.filter_by(answer_id=self.id, vote_type='downvote').count()
        return upvotes - downvotes
