from config import SQLALCHEMY_DATABASE_URI
from app import db
import os.path

#Creates the database and tables
db.create_all()
