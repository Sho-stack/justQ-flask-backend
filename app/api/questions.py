from flask import Blueprint, request, jsonify
from app.models import Question, Answer, User, Vote
from app import db
from flask_login import login_required, current_user
from datetime import datetime
from translate import Translator
import langid
from sqlalchemy import asc, desc



questions_bp = Blueprint('questions', __name__)

async def translate_async(content):
    # Get the source language and target languages
    source_lang = langid.classify(content)[0]
    target_languages = ['zh-CN', 'es', 'hi', 'ar', 'pt', 'bn', 'ru', 'ja', 'pa', 'pl']
    translations = {}

    # First, translate the content to English if it's not already in English
    if source_lang != 'en':
        translator_to_english = Translator(from_lang=source_lang, to_lang='en')
        english_translation = translator_to_english.translate(content)
    else:
        english_translation = content

    translations['en'] = english_translation

    # Generate translations for each target language using the English translation as the source
    for target_lang in target_languages:
        translator = Translator(from_lang='en', to_lang=target_lang)
        translation = translator.translate(english_translation)
        translations[target_lang] = translation

    return translations

async def save_question_translations(question_id, content):
    translations = await translate_async(content)
    question = Question.query.get(question_id)
    
    question.content_en = translations['en']
    question.content_pl = translations['pl']
    question.content_es = translations['es']
    question.content_zh = translations['zh-CN']
    question.content_hi = translations['hi']
    question.content_ar = translations['ar']
    question.content_pt = translations['pt']
    question.content_bn = translations['bn']
    question.content_ru = translations['ru']
    question.content_ja = translations['ja']
    question.content_pa = translations['pa']
    db.session.commit()

async def save_answer_translations(answer_id, content):
    translations = await translate_async(content)
    answer = Answer.query.get(answer_id)

    answer.content_en = translations['en']
    answer.content_pl = translations['pl']
    answer.content_es = translations['es']
    answer.content_zh = translations['zh-CN']
    answer.content_hi = translations['hi']
    answer.content_ar = translations['ar']
    answer.content_pt = translations['pt']
    answer.content_bn = translations['bn']
    answer.content_ru = translations['ru']
    answer.content_ja = translations['ja']
    answer.content_pa = translations['pa']

    db.session.commit()

@questions_bp.route('/questions', methods=['GET'])
def get_all_questions():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'timestamp', type=str)
    order = request.args.get('order', 'desc', type=str)

    if order not in ['asc', 'desc']:
        return jsonify({'error': 'Invalid order value'}), 400

    order_func = asc if order == 'asc' else desc

    if sort_by == 'total_score':
        questions = Question.query.order_by(order_func(Question.total_score)).paginate(page=page, per_page=per_page, error_out=False)
    else:
        questions = Question.query.order_by(order_func(Question.timestamp)).paginate(page=page, per_page=per_page, error_out=False)

    output = []

    user = current_user  # get the current user explicitly
    print('current user in questions.py /questions GET: ', user)

    for question in questions:
        user_vote = 0
        if current_user.is_authenticated:
            vote = Vote.query.filter_by(user_id=current_user.id, question_id=question.id).first()
            print(vote)
            if vote:
                if vote.vote_type == 'upvote':
                    user_vote = 1
                elif vote.vote_type == 'downvote':
                    user_vote = -1

        print(user_vote)

        question_data = {
            'id': question.id,
            'content': question.content,
            'content_en': question.content_en or '',
            'content_pl': question.content_pl or '',
            'content_es': question.content_es or '',
            'content_zh': question.content_zh or '',
            'content_hi': question.content_hi or '',
            'content_ar': question.content_ar or '',
            'content_pt': question.content_pt or '',
            'content_bn': question.content_bn or '',
            'content_ru': question.content_ru or '',
            'content_ja': question.content_ja or '',
            'content_pa': question.content_pa or '',
            'timestamp': question.timestamp,
            'user_id': question.user_id,
            'author': question.author.username,
            'net_votes': question.total_score,
            'user_vote': user_vote,

        }
        output.append(question_data)

    return jsonify({'questions': output, 'total_pages': questions.pages, 'current_page': questions.page})


@questions_bp.route('/questions/<int:question_id>/answers', methods=['GET'])
def get_answers(question_id):
    question = Question.query.get(question_id)

    if not question:
        return jsonify({'error': 'Invalid question ID'}), 400

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    answers = question.answers.order_by(Answer.timestamp).paginate(page=page, per_page=per_page, error_out=False)
    output = []

    for answer in answers:
        user_vote = 0
        if current_user.is_authenticated:
            vote = Vote.query.filter_by(user_id=current_user.id, answer_id=answer.id).first()
            if vote:
                if vote.vote_type == 'upvote':
                    user_vote = 1
                elif vote.vote_type == 'downvote':
                    user_vote = -1

        answer_data = {
            'id': answer.id,
            'content': answer.content,
            'content_en': answer.content_en or '',
            'content_pl': answer.content_pl or '',
            'content_es': answer.content_es or '',
            'content_zh': answer.content_zh or '',
            'content_hi': answer.content_hi or '',
            'content_ar': answer.content_ar or '',
            'content_pt': answer.content_pt or '',
            'content_bn': answer.content_bn or '',
            'content_ru': answer.content_ru or '',
            'content_ja': answer.content_ja or '',
            'content_pa': answer.content_pa or '',
            'timestamp': answer.timestamp,
            'user_id': answer.user_id,
            'author': answer.author.username,
            'question_id': answer.question_id,
            'net_votes': answer.get_votes(),
            'user_vote': user_vote  # Add this line
        }
        output.append(answer_data)

    return jsonify({'answers': output, 'total_pages': answers.pages, 'current_page': answers.page})


@questions_bp.route('/questions', methods=['POST'])
@login_required
async def add_question():
    data = request.get_json()
    content = data.get('content')

    if not content:
        return jsonify({'error': 'Content is required'}), 400

    new_question = Question(content=content, author=current_user, timestamp=datetime.utcnow())
    db.session.add(new_question)
    db.session.commit()

    # Start a new event loop to call the asynchronous translation function
    await save_question_translations(new_question.id, content)

    return jsonify({'message': 'Question added successfully', 'question': {
        'id': new_question.id,
        'content': new_question.content,
        'timestamp': new_question.timestamp,
        'user_id': new_question.user_id,
        'author': new_question.author.username,
        'net_votes': new_question.get_votes()
    }}), 201



@questions_bp.route('/answers', methods=['POST'])
@login_required
async def add_answer():
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

    # Start a new event loop to call the asynchronous translation function
    await save_answer_translations(new_answer.id, content)

    return jsonify({'message': 'Answer added successfully', 'answer': {
        'id': new_answer.id,
        'content': new_answer.content,
        'content_en': new_answer.content_en,
        'content_pl': new_answer.content_pl,
        'content_es': new_answer.content_es,
        'content_zh': new_answer.content_zh,
        'content_hi': new_answer.content_hi,
        'content_ar': new_answer.content_ar,
        'content_pt': new_answer.content_pt,
        'content_bn': new_answer.content_bn,
        'content_ru': new_answer.content_ru,
        'content_ja': new_answer.content_ja,
        'content_pa': new_answer.content_pa,
        'timestamp': new_answer.timestamp,
        'user_id': new_answer.user_id,
        'author': new_answer.author.username,
        'net_votes': new_answer.get_votes()
    }}), 201


@questions_bp.route('/vote', methods=['PUT'])
@login_required
def update_vote():
    data = request.get_json()
    vote_value = data.get('vote')
    question_id = data.get('question_id')
    answer_id = data.get('answer_id')

    if vote_value not in [-1, 0, 1]:
        return jsonify({'error': 'Invalid vote value'}), 400

    if question_id is None and answer_id is None:
        return jsonify({'error': 'Either question_id or answer_id must be provided'}), 400

    if question_id is not None and answer_id is not None:
        return jsonify({'error': 'Only one of question_id or answer_id can be provided'}), 400

    if question_id:
        obj = Question.query.get(question_id)
        if not obj:
            return jsonify({'error': 'Invalid question ID'}), 400

        vote = Vote.query.filter_by(user_id=current_user.id, question_id=question_id).first()

    if answer_id:
        obj = Answer.query.get(answer_id)
        if not obj:
            return jsonify({'error': 'Invalid answer ID'}), 400

        vote = Vote.query.filter_by(user_id=current_user.id, answer_id=answer_id).first()

    if vote_value == 0:
        if vote:
            db.session.delete(vote)
            db.session.commit()
        else:
            return jsonify({'message': 'No vote to remove'}), 204
    else:
        if not vote:
            if question_id:
                vote = Vote(user_id=current_user.id, question_id=question_id, timestamp=datetime.utcnow())
            else:
                vote = Vote(user_id=current_user.id, answer_id=answer_id, timestamp=datetime.utcnow())

            db.session.add(vote)

        vote.vote_type = 'upvote' if vote_value == 1 else 'downvote'
        vote.timestamp = datetime.utcnow()

    if question_id:
        upvotes = Vote.query.filter_by(question_id=question_id, vote_type='upvote').count()
        downvotes = Vote.query.filter_by(question_id=question_id, vote_type='downvote').count()
        answers = Answer.query.filter_by(question_id=question_id).count()
        obj.total_score = upvotes - downvotes + answers

    db.session.commit()

    return jsonify({'message': 'Vote updated successfully'}), 200