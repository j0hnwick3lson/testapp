import datetime
import base64
import hashlib
import time
import json
from testapp import db,login_manager
from flask import current_app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        payload = {
            'user_id': self.id,
            'exp': time.time() + expires_sec
        }
        token_bytes = json.dumps(payload).encode('utf-8')
        token = base64.urlsafe_b64encode(token_bytes).rstrip(b'=').decode('utf-8')
        return token


    @staticmethod
    def verify_reset_token(token, max_age=1800):
        try:
            token = token.encode('utf-8')
            token += b'=' * ((4 - len(token) % 4) % 4)
            token_bytes = base64.urlsafe_b64decode(token)
            payload = json.loads(token_bytes.decode('utf-8'))
            user_id = payload['user_id']
            exp_time = payload['exp']
            if time.time() > exp_time:
                return None
            return User.query.get(user_id)
        except (ValueError, KeyError, json.JSONDecodeError):
            return None 
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Announcement(db.Model):
    date_post = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    announce = db.Column(db.Text,nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    
    def __repr__(self):
        return f"Announcement('{self.announce}','{self.date_post}')"