from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                                                            Length, EqualTo)
from models import User


# Raises ValidationError if username already exists.
def name_exists(form, field):

    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User with that name already exists.')


# Raises ValidationError if email already exists.
def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')


# Registration form for new users.
class RegisterForm(FlaskForm):

    username = StringField(
        'Username',
        validators = [
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters, "
                                    "numbers, and underscores only.")),
            name_exists
        ])

    email = StringField(
        'Email',
        validators = [
            DataRequired(),
            Email(),
            email_exists
        ])

    password = PasswordField(
        'Password',
        validators = [
            DataRequired(),
            Length(min=8),
            EqualTo('password2', message='Passwords must match.')
        ])

    password2 = PasswordField(
            'Confirm Password',
            validators = [DataRequired()
        ])


# Login form for existing users.
class LoginForm(FlaskForm):

    email = StringField(
        'Email',
        validators = [
            DataRequired(),
            Email()
        ])

    password = PasswordField(
        'Password',
        validators = [
            DataRequired(),
            Length(min=8),
        ])


# Edit profile form for existing users.
class ProfileForm(FlaskForm):

    about = StringField(
        'About')

    twitter = StringField(
        'Twitter URL')

    facebook = StringField(
        'Facebook URL')

    instagram = StringField(
        'Instagram URL')
