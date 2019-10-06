from flask import Flask, render_template, session, flash, redirect, url_for
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

manager = Manager(app)
bootstrap = Bootstrap(app)

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

Form = FlaskForm
class NameForm(Form):
    name = StringField('Your name', validators=[DataRequired()])

if __name__ == "__main__":
    app.run(debug=True) 
    #manager.run()