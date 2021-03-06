from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restful import Api
import os


# remember flash messages for form submit success for task submission

currentDirectory = os.getcwd()
UPLOAD_FOLDER = currentDirectory + "\\" + "uploads"




app = Flask(__name__)
app.config['SECRET_KEY'] = '057cb5e668fe15fefb0680eee12956cd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


api = Api(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from wraithc2 import routes
from wraithc2.resources import AgentEndpoint, KeysEndpoint

api.add_resource(AgentEndpoint, '/api')
api.add_resource(KeysEndpoint, '/keys')
