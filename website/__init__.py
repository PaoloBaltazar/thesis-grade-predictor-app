from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'thesisgradepredictorapp'
  app.config['SQLALCHEMY_DATABASE_URI']  = f'sqlite:///{DB_NAME}' #where data base is stored
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



