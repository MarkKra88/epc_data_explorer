from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from app.routes import main
from app.db_utils import reset_database
import os


load_dotenv()

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(main)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    from app.models import db
    db.init_app(app)

    with app.app_context():
        reset_database()
        from app.models import APIResult, ScraperResult
        db.create_all()  # Create tables if they don't exist

    return app
