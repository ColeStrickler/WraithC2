from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from wraithc2.models import User


class SignInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    # EqualTo(var) validator to confirm that password value is correct


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    register = SubmitField('Register User')
    # EqualTo(var) validator to confirm that password value is correct


class TaskForm(FlaskForm):
    command = StringField('Command', validators=[DataRequired()])
    agent = StringField('Agent #', validators=[DataRequired()])
    parameters = StringField('Command parameters') # , validators=[DataRequired()] was here
    sendTask = SubmitField('Send Task', validators=[DataRequired()])

class StatusForm(FlaskForm):
    agent = StringField('Agent #', validators=[])
    result = StringField('Task Status')
    search = SubmitField('Search', validators=[DataRequired()])