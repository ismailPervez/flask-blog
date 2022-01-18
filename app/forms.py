from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
'''
DataRequired validator prevents the user from leaving a field blank
Length validator prevents a user from submitting data with characters less that the
min value specified and more that the max value specified
'''
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from wtforms.widgets import TextArea

class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[
        DataRequired(),
        Length(min=3, max=30)
    ])

    email = StringField('email', validators=[
        DataRequired(),
        Email()
    ])

    password = PasswordField('password', validators=[DataRequired()])

    confirm_password = PasswordField('confirm password', validators=[
        DataRequired(),
        EqualTo('password')
    ])

    submit = SubmitField('sign up')

    '''
    custom validation error to check if the username or the email already exists 
    in the database
    '''
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("username already exists!")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("email is already taken!")

class LoginForm(FlaskForm):
    username = StringField('username', validators=[
        DataRequired(),
        Length(min=3, max=30)
    ])

    password = PasswordField('password', validators=[DataRequired()])

    submit = SubmitField('log in')

# create new post article form
class CreatePost(FlaskForm):
    title = StringField('title', validators=[
        DataRequired(),
        Length(min=10, max=100)
    ])

    content = StringField('content', validators=[
        DataRequired(),
        Length(min=20, max=400)
    ], widget=TextArea())

    '''
    make sure to inform the user to seperate the tags using spaces
    '''
    tags = StringField('tags', validators=[
        DataRequired(),
        Length(min=10, max=100)
    ])

    submit = SubmitField('create post')

# create new post article form
class UpdatePost(FlaskForm):
    title = StringField('title', validators=[
        DataRequired(),
        Length(min=10, max=100)
    ])

    content = StringField('content', validators=[
        DataRequired(),
        Length(min=20, max=400)
    ], widget=TextArea())

    '''
    make sure to inform the user to seperate the tags using spaces
    '''
    tags = StringField('tags', validators=[
        DataRequired(),
        Length(min=10, max=100)
    ])

    submit = SubmitField('update post')
