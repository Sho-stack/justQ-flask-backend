from flask import Blueprint, request, jsonify
from app.models import Question, Answer, User, Vote
from app import db
from flask_login import login_required, current_user
from datetime import datetime
from translate import Translator
import langid
import asyncio
from aiohttp import ClientSession


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

async def save_translations(question_id, content):
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

@questions_bp.route('/questions', methods=['GET'])
def get_all_questions():
    questions = Question.query.order_by(Question.timestamp.desc()).all()
    output = []

    for question in questions:
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

    # Start a new event loop to call the asynchronous translation function
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(save_translations(new_question.id, content))

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

    return jsonify({'message': 'Question added successfully', 'question': {
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
        'content_id': new_answer.content_id,
        'timestamp': new_answer.timestamp,
        'user_id': new_answer.user_id,
        'author': new_answer.author.username,
        'net_votes': new_answer.get_votes()
    }}), 201


