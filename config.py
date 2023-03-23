import os

class Config:
    SECRET_KEY = 'some-secret-key'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://michalszostak:burzuj123@michalszostak.mysql.pythonanywhere-services.com:3306/michalszostak$justq'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
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