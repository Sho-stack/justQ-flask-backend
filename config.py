import os

class Config:

    # MySQL configuration
    MYSQL_USER = 'michalszostak'
    MYSQL_PASSWORD = 'Burzuj123!'
    MYSQL_DATABASE = 'michalszostak$justq'
    MYSQL_HOST = 'michalszostak.mysql.pythonanywhere-services.com'
    MYSQL_PORT = 3306

    # Set SQLALCHEMY_DATABASE_URI to use the MySQL configuration
    SQLALCHEMY_DATABASE_URI = f'mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'

    SECRET_KEY = 'some-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REMEMBER_COOKIE_DURATION = 3600

    # Email configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'justq.main@gmail.com'
    MAIL_PASSWORD = 'aqijdaltmxygxane'

    # URL for front-end consumer
    FRONT_END_BASE_URL = 'https://sho-stack.github.io/justQ-react-frontend/'

