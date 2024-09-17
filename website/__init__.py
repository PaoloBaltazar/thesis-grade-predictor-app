from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    
    # Securely load sensitive configurations
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///default.db')
    
    db.init_app(app)

    # Register blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Create database and add initial users
    from .db_model import User
    from .initial_users import add_initial_users

    create_database(app)
    add_initial_users(app)

    # Login management
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    # Only useful for SQLite in local development
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')
