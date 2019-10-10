#!/usr/bin/env python
import os
from flask import current_app
from application import create_app, db
from application.models import User, Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
import unittest

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """Run the unit tests."""
    tests = unittest.TestLoader().discover('application/main/tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()


# from flask import Flask, render_template, session, flash, redirect, url_for
# from flask_script import Manager
# from flask_bootstrap import Bootstrap
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField, PasswordField
# from wtforms.validators import DataRequired
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate, MigrateCommand
# from flask_mail import Mail, Message
# import os

# basedir = os.path.abspath(os.path.dirname(__file__))

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'hard to guess string'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# manager = Manager(app)
# bootstrap = Bootstrap(app)
# migrate = Migrate(app, db)
# manager.add_command('db', MigrateCommand)
# mail = Mail(app)

# app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/quick-form', methods=['GET', 'POST'])
# def quick_form():
#     form = NameForm()
#     if form.validate_on_submit():
#         old_name = session.get('name')                   
#         if old_name is not None and old_name != form.name.data: 
#             flash('Looks like you have changed your name!')
#         session['name'] = form.name.data
#         form.name.data = ''
#         return redirect(url_for('quick_form'))
#     return render_template('quick-form.html', form=form, name=session.get('name'))

# @app.route('/login', methods=['GET', 'POST'])
# def login_form():
#     loginform = LoginForm()
#     if loginform.validate_on_submit():
#         user = User.query.filter_by(username=loginform.username.data, password=loginform.password.data).first()
#         if user is None:
#             return '<h3>Invalid Username or Password</h3>'
#         else:
#             session['known'] = True
#         session['username'] = loginform.username.data
#         loginform.username.data = ''
#         return redirect(url_for('login_form'))
#     return render_template('login-form.html', loginform = loginform, username = session.get('username'), known = session.get('known', False))

# Form = FlaskForm
# login_form = FlaskForm

# class NameForm(Form):
#     name = StringField('Your name', validators=[DataRequired()])

# class LoginForm(Form):
#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     submit = SubmitField()

# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key = True)
#     roleName = db.Column(db.String(64), unique=True)
#     users = db.relationship('User', backref='role')

#     def __repr__(self):
#         return '<Role %r>' % self.name

# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key = True)
#     username = db.Column(db.String(64), unique=True, index=True)
#     password = db.Column(db.String(64))
#     role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

#     def __repr__(self):
#         return '<User %r>' % self.username

# if __name__ == "__main__":
#     app.run(debug=True) 
#     #manager.run()