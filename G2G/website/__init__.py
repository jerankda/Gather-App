from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Initialize SQLAlchemy and set database name
db = SQLAlchemy()
DB_NAME = "database.db"

# Function to create the Flask app
def create_app():
    app = Flask(__name__)

    # Configuration settings
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Importing blueprints for different parts of the app
    from .views import views
    from .auth import auth
    from .create import create
    from . map_marker import map_marker
    from . find_gather import find_gather
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(create,url_prefix='/')
    app.register_blueprint(map_marker, url_prefix='/')
    app.register_blueprint(find_gather, url_prefix='/')
    # Import User model and create database tables
    from .models import User
    with app.app_context():
        db.create_all()

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Define function to load user for Flask-Login
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# Function to create the database if it doesn't exist
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
