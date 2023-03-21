from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        from app.api import questions, auth
        app.register_blueprint(questions.questions_bp)
        app.register_blueprint(auth.auth_bp)

    return app