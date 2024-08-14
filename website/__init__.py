from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

def create_app():

  db = SQLAlchemy()
  DB_NAME = "database.db"

  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'thesisgradepredictorapp'
  app.config['SQLALCHEMY_DATABASE_URI']  = f'sqlite:///{DB_NAME}' #where data base is stored

  from .views import views
  from .auth import auth

  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')

  return app

