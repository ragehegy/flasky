from datetime import datetime
from flask import render_template, session, redirect, url_for, flash
from . import main
from .forms import NameForm, LoginForm
from .. import db
from ..models import User

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/quick-form', methods=['GET', 'POST'])
def quick_form():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')                   
        if old_name is not None and old_name != form.name.data: 
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('quick_form'))
    return render_template('quick-form.html', form=form, name=session.get('name'))

@main.route('/login', methods=['GET', 'POST'])
def login_form():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        user = User.query.filter_by(username=loginform.username.data, password=loginform.password.data).first()
        if user is None:
            return '<h3>Invalid Username or Password</h3>'
        else:
            session['known'] = True
        session['username'] = loginform.username.data
        loginform.username.data = ''
        return redirect(url_for('login_form'))
    return render_template('login-form.html', loginform = loginform, username = session.get('username'), known = session.get('known', False))
