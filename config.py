import os


class Config:
    SECRET_KEY = os.environ.get("secret_key")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///portfolio.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('main_mail')
    MAIL_PASSWORD = os.environ.get('mail_password')
    MAIL_DEFAULT_SENDER = os.environ.get('main_mail')
    UPLOADED_IMAGES_DEST = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/images')
