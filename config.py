import os
from dotenv import load_dotenv

class Config:
    
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
    MYSQL_USER = os.environ.get("MYSQL_USER")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
    MYSQL_DATABASE = os.environ["MYSQL_DATABASE"]
    MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE")
    MYSQL_HOST = os.environ.get("MYSQL_HOST")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    

    # Set SQLALCHEMY_DATABASE_URI to use the MySQL configuration
    SQLALCHEMY_DATABASE_URI = f'mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REMEMBER_COOKIE_DURATION = 3600

    # Email configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True

    # URL for front-end consumer (used in password reset email)
    FRONT_END_BASE_URL = 'https://justq-react.herokuapp.com/'
