from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, FileField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User
from sqlalchemy.orm import scoped_session, sessionmaker, Query
from flask import current_app
from .. import db

class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')

class RegistrationForm(Form):
    first_name = StringField('First Name', validators=[Required(), Length(1, 64)])
    last_name = StringField('Last Name', validators=[Required(), Length(1, 64)])
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('Username', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, ''numbers, dots or underscores')])
    password = PasswordField('Password', validators=[Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    phone = StringField('Phone', validators=[Required(), Length(1, 64), Regexp('^[0-9+\(\)#\.\s\/ext-]+$', 0, 'Phones must have only numbers, ''numbers')])
    user_type = RadioField('Type', choices=[('Teacher','Teacher'),('Student','Student')])
    govern = StringField('Govern', validators=[Required(), Length(1, 64)])
    photo = FileField('Photo', validators=[])
    submit = SubmitField('Register')

    def validate_username(self, field):
        if db.session.query(User).filter_by(username=field.data).first():
           raise ValidationError('Username already in use.')

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).first():
           raise ValidationError('Email already exist.')

class ChangePasswordForm(Form):
    old_password = PasswordField('Old password', validators=[Required()])
    password = PasswordField('New password', validators=[Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm new password', validators=[Required()])
    submit = SubmitField('Update Password')


class PasswordResetRequestForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(Form):
    password = PasswordField('New Password', validators=[Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Reset Password')


class ChangeEmailForm(Form):
    email = StringField('New Email', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Update Email Address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')