from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_prediction_id = db.Column(db.Integer)  # User-specific prediction ID
    attendance = db.Column(db.Float)
    previousGrade = db.Column(db.Float)
    financialSituation = db.Column(db.Float)
    learningEnvironment = db.Column(db.Float)
    gradeLevel = db.Column(db.Integer)
    predictedGrade = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('data', lazy=True))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150))
    password = db.Column(db.String(150))
