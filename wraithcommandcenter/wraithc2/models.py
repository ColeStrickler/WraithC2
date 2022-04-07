from datetime import datetime
from wraithc2 import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader  # set up flask-login
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin): # inherit UserMixin to manage sessions
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False) # 20 = max length
    password = db.Column(db.String(60), nullable=False) # hashing algo makes len 60
    tasks = db.relationship('Tasks', backref='owner', lazy=True)
    # Tasks is uppercase becasue it is a class reference

    def __repr__(self): # defines how object is printed out
        return f"User:{self.username}, ID: {self.id}"


class Tasks(db.Model):
    __tablename__ = 'tasks'
    time = db.Column(db.String(), default=str(datetime.utcnow()), primary_key=True)
    result = db.Column(db.String(), default="PENDING")
    command = db.Column(db.String(), nullable=False)
    agent = db.Column(db.String(), nullable=False)
    author = db.Column(db.String(), db.ForeignKey('users.username'))
    feedback = db.Column(db.String(), default="PENDING")
    # reference user.id is lowercase because it is a table reference

    def __repr__(self): # defines how object is printed out
        return f"[Agent:{self.agent}   Time:{self.time}   Command:{self.command}   Feedback:{self.feedback}   User:{self.author}   Status:{self.result}]"


class Keys(db.Model):
    __tablename__ = 'keys'
    keys = db.Column(db.String(), nullable=False, primary_key=True)
