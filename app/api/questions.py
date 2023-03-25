from flask import Blueprint, request, jsonify
from app.models import Question, User, Vote
from app import db
from flask_login import login_required, current_user
from datetime import datetime

questions_bp = Blueprint('questions', __name__)

@questions_bp.route('/questions', methods=['GET'])
def get_all_questions():
    questions = Question.query.order_by(Question.timestamp.desc()).all()
    output = []

    for question in questions:
        question_data = {
            'id': question.id,
            'content': question.content,
            'timestamp': question.timestamp,
            'user_id': question.user_id,
            'author': question.author.username,
            'net_votes': question.get_votes()
        }
        output.append(question_data)

    return jsonify({'questions': output})

@questions_bp.route('/questions', methods=['POST'])
@login_required
def add_question():
    data = request.get_json()
    content = data.get('content')

    if not content:
        return jsonify({'error': 'Content is required'}), 400

    new_question = Question(content=content, author=current_user, timestamp=datetime.utcnow())
    db.session.add(new_question)
    db.session.commit()

    return jsonify({'message': 'Question added successfully', 'question': {
        'id': new_question.id,
        'content': new_question.content,
        'timestamp': new_question.timestamp,
        'user_id': new_question.user_id,
        'author': new_question.author.username,
        'net_votes': new_question.get_votes()
    }}), 201
