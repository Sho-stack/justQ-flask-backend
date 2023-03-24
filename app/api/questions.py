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

from flask import Blueprint, request, jsonify
from app.models import Question, User, Vote, Answer
from app import db
from flask_login import login_required, current_user
from datetime import datetime

questions_bp = Blueprint('questions', __name__)

# ... existing code ...


@questions_bp.route('/questions/<int:question_id>/answers', methods=['POST'])
@login_required
def add_answer(question_id):
    data = request.get_json()
    content = data.get('content')

    if not content:
        return jsonify({'error': 'Content is required'}), 400

    question = Question.query.get(question_id)

    if not question:
        return jsonify({'error': 'Question not found'}), 404

    new_answer = Answer(content=content, author=current_user, question=question, timestamp=datetime.utcnow())
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


@questions_bp.route('/<content_type>/<int:content_id>/vote', methods=['POST'])
@login_required
def vote(content_type, content_id):
    data = request.get_json()
    vote_type = data.get('vote_type')

    if not vote_type or vote_type not in ['upvote', 'downvote']:
        return jsonify({'error': 'Vote type is required and must be either "upvote" or "downvote"'}), 400

    if content_type not in ['question', 'answer']:
        return jsonify({'error': 'Invalid content type'}), 400

    content = Question.query.get(content_id) if content_type == 'question' else Answer.query.get(content_id)

    if not content:
        return jsonify({'error': f'{content_type.capitalize()} not found'}), 404

    existing_vote = Vote.query.filter_by(user_id=current_user.id, **{f'{content_type}_id': content_id}).first()

    if existing_vote:
        if existing_vote.vote_type == vote_type:
            return jsonify({'error': 'You have already voted this way'}), 400
        else:
            existing_vote.vote_type = vote_type
    else:
        new_vote = Vote(user=current_user, vote_type=vote_type, **{f'{content_type}_id': content_id},
                        timestamp=datetime.utcnow())
        db.session.add(new_vote)

    db.session.commit()

    return jsonify({'message': 'Vote added successfully', 'net_votes': content.get_votes()}), 201

