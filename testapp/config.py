import os
from flask_bcrypt import Bcrypt
import secrets

class Config:
    SECRET_KEY = '1d1711eef7b361162bdc6fd295107865648d3392'
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=465
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWD')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
