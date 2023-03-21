from flask import Blueprint, request, jsonify
from app.models import Question, Answer
from app import db

questions_bp = Blueprint('questions', __name__)

@questions_bp.route('/questions', methods=['POST'])
def add_question():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({'error': 'Title and content are required'}), 400

    question = Question(title=title, content=content)
    db.session.add(question)
    db.session.commit()

    return jsonify(question.to_dict()), 201

# Add more routes for handling answers, upvotes, and other question-related actions