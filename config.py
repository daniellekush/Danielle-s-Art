import os

#Determines whether CSRF prevention should be enabled (True = enabled)
WTF_CSRF_ENABLED = True
#The secret key used to create secure tokens
SECRET_KEY = 'a-very-secretive-key'

#This informs where SQLAlchemy will put the database file
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True

