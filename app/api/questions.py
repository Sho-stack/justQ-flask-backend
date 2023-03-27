from flask import Blueprint, request, jsonify
from app.models import Question, Answer, User, Vote
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

@questions_bp.route('/questions/<int:question_id>/answers', methods=['GET'])
def get_answers(question_id):
    question = Question.query.get(question_id)

    if not question:
        return jsonify({'error': 'Invalid question ID'}), 400

    answers = question.answers.order_by(Answer.timestamp).all()
    output = []

    for answer in answers:
        answer_data = {
            'id': answer.id,
            'content': answer.content,
            'timestamp': answer.timestamp,
            'user_id': answer.user_id,
            'author': answer.author.username,
            'question_id': answer.question_id,
            'net_votes': answer.get_votes()
        }
        output.append(answer_data)

    return jsonify({'answers': output})

@questions_bp.route('/answers', methods=['POST'])
@login_required
def add_answer():
    data = request.get_json()
    content = data.get('content')
    question_id = data.get('question_id')

    if not content or not question_id:
        return jsonify({'error': 'Content and question ID are required'}), 400

    question = Question.query.get(question_id)
    if not question:
        return jsonify({'error': 'Invalid question ID'}), 400

    new_answer = Answer(content=content, author=current_user, timestamp=datetime.utcnow(), question_id=question_id)
    db.session.add(new_answer)
    db.session.commit()

    return jsonify({'message': 'Answer added successfully', 'answer': {
        'id': new_answer.id,
        'content': new_answer.content,
        'timestamp': new_answer.timestamp,
        'user_id': new_answer.user_id,
        'author': new_answer.author.username,
        'question_id': new_answer.question_id,
        'net_votes': new_answer.get_votes()
    }}), 201