from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Mail
from config import Config
import subprocess
from flask_sslify import SSLify

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, origins="*", supports_credentials=True)
    
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    sslify = SSLify(app)

    from app.api import questions, auth
    app.register_blueprint(questions.questions_bp)
    app.register_blueprint(auth.auth_bp)

    @app.route('/update_from_github', methods=['POST'])
    def update():
        subprocess.call(["/home/michalszostak/update_repo.sh"])
        return "Repository updated", 200

    return app
