from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'thesisgradepredictorapp'
  app.config['SQLALCHEMY_DATABASE_URI']  = os.getenv('DATABASE_URL', 'postgres://thesis_database_user:77GHKgFXEYDY0atVLc0APBxUhkMJmOSR@dpg-crktbtrv2p9s7e7cgm0-a:5432/thesis_database')
  db.init_app(app)

  from .views import views
  from .auth import auth

  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')

  from .db_model import User
  from .initial_users import add_initial_users

  create_database(app)
  add_initial_users(app)

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)


  #Telling flask how we load user and look for the primary key
  @login_manager.user_loader
  def load_user(id):
    return User.query.get(int(id))

  return app

def create_database(app):
  if not path.exists('website/' + DB_NAME):
    with app.app_context():
      db.create_all()
    print('Created Database!')



