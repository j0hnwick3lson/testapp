import secrets
import os
from PIL import Image
from flask import url_for,current_app
from flask_mail import Message
from testapp import mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,fxt_ext=os.path.splitext(form_picture.filename)
    picture_fn=random_hex+fxt_ext
    picture_path=os.path.join(current_app.root_path,'static\pictures',picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path) 
    return picture_fn

def send_reset_email(user):
    token=user.get_reset_token()
    msg=Message("Password Reset Request",
                sender='noreply@demo.com',
                recipients=[user.email])
    msg.body=f""" To Reset Your password , visit the following Link:
    { url_for('users.reset_token',token=token,_external=True) }"""
    mail.send(message=msg)
