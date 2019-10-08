from flask_mail import Message, Mail
from hello import mail, app

msg = Message('Test Mail', sender='mhmdrgh@gmail.com', recipients=['mhmdrgh@gmail.com'])
msg.body = 'This is a Flask_Mail test'
with app.app_context():
    mail.send(msg)