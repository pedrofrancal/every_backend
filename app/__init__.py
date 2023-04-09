from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Create an instance of the SQLAlchemy class
db = SQLAlchemy()

# Function to create and configure the Flask app


def create_app(testing=False):
    app = Flask(__name__)

    # Configure app with environment variables
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Use an in-memory SQLite database for testing, or SQL Server when not testing
    if testing:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

    # Initialize the database with the app
    db.init_app(app)

    # Import and register blueprints for routes
    from app.routes import shop, user
    app.register_blueprint(shop.bp)
    app.register_blueprint(user.bp)

    return app
