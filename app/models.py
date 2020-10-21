from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from . import login_manager
from . import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

engine = create_engine('mysql://root:@localhost/academic', convert_unicode=True, echo=False)
Base = declarative_base()
Base.metadata.reflect(engine)

class User(UserMixin, Base):
    __table__ = Base.metadata.tables['user']
    
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.user_id})

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def id(self):
        """Return an identifier."""
        return self.user_id

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.status = "active"
        db.session.add(self)
        return True
        
class Teacher(Base):
    __table__ = Base.metadata.tables['teacher']

class Student(Base):
    __table__ = Base.metadata.tables['student']

class Course(Base):
    __table__ = Base.metadata.tables['course']


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))