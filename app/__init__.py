from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging

#New Flask application object
app = Flask(__name__)
logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
app.config.from_object('config')
#Instance of the database object
db = SQLAlchemy(app)

#Manages database migrations
migrate = Migrate(app, db)

#Imports the views module which produces dynamic content for the user
#and models to store in the database
from app import views, models

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view =  "login"
login_manager.login_message_category = "error"

@login_manager.user_loader
def load_user(userid):
    return models.User.query.filter(models.User.id==userid).first()
