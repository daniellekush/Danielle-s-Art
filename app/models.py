from flask_login import UserMixin
from app import db

PageSuggestion = db.Table(
                  'PageSuggestion',
                  db.Column('suggestion', db.Integer, db.ForeignKey('Suggestion.id'), primary_key=True),
                  db.Column('owner', db.Integer, db.ForeignKey('User.id'))
)

class Suggestion(db.Model):
    __tablename__ = "Suggestion"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sType = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    desc = db.Column(db.String, nullable=False)
    suggestions = db.relation(
         'Suggestion', secondary=PageSuggestion,
         primaryjoin=PageSuggestion.c.suggestion == id,
         backref="suggests")

class User(UserMixin, db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))
    users = db.relation(
         'User', secondary=PageSuggestion,
         primaryjoin=PageSuggestion.c.owner == id,
         backref="registers")
