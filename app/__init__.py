from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

def create_app():
    # Load environment variables
    load_dotenv()

    # Create and configure the app
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    # Configure app
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['OPENMRS_BASE_URL'] = os.getenv('OPENMRS_BASE_URL')
    app.config['OPENMRS_USERNAME'] = os.getenv('OPENMRS_USERNAME')
    app.config['OPENMRS_PASSWORD'] = os.getenv('OPENMRS_PASSWORD')
    app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

    # Register blueprints
    from app.routes import api
    app.register_blueprint(api, url_prefix='/api')

    return app
