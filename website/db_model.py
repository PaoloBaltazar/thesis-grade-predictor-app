from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Data(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  attendance = db.Column(db.Integer)
  previousGrade = db.Column(db.Integer)
  financialSituation = db.Column(db.Integer)
  learningEnvironment = db.Column(db.Integer)

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(150), unique=True)
  name = db.Column(db.String(150))
  password = db.Column(db.String(150))

