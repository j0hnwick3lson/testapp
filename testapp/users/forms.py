from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,EqualTo,ValidationError,Email,Length
from flask_wtf.file import file_allowed,FileField
from flask_wtf import FlaskForm
from flask_login import current_user
from testapp.models import User


class registration_form(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=10)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('sign up')
    
    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This Username has been already Taken. so choose Another one')
        
    def validate_email(self,email):
        email=User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('This Email has been already used. so choose Another one')
        
class login_form(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Login')
    
    
    
class updateform(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=10)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    picture= FileField('Update Profile Picture',validators=[file_allowed(['jpg','png','jpeg'])])
    submit=SubmitField('Update')
    
    def validate_username(self,username):
        if username.data != current_user.username:
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This Username has been already Taken. so choose Another one')
        
    def validate_email(self,email):
        if email.data != current_user.email:
            email=User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('This Email has been already used. so choose Another one')

class Requestresetform(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    submit=SubmitField('Reset Password reset')
    
    def validate_email(self,email):
        email=User.query.filter_by(email=email.data).first()
        if email is None:
                raise ValidationError('There is no account with that username.You Must register first')
            
            
class Resetpasswordform(FlaskForm):
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('reset password')

class AnnouncementForm(FlaskForm):
    announce=TextAreaField("announce",validators=[DataRequired()])
    submit= SubmitField('Post')
