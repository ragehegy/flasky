from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    # attach routes and custom error pages here
    
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/quick-form', methods=['GET', 'POST'])
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

    @app.route('/login', methods=['GET', 'POST'])
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

    Form = FlaskForm
    login_form = FlaskForm

    class NameForm(Form):
        name = StringField('Your name', validators=[DataRequired()])

    class LoginForm(Form):
        username = StringField('Username', validators=[DataRequired()])
        password = PasswordField('Password', validators=[DataRequired()])
        submit = SubmitField()

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app