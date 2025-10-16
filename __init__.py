# File: app/__init__.py
import os
import sys
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

# Load environment variables early
from dotenv import load_dotenv
load_dotenv()

# Add the project's root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config import config

# Initialize extensions globally
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()

def create_app(config_name=None):
    """Application factory function."""
    app = Flask(__name__)

    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')

    config_object = config.get(config_name, config['default'])
    app.config.from_object(config_object)

    # Initialize extensions with the app instance
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    # --- Swagger UI Configuration ---
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'

    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path)

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "WhatsApp API Module"}
    )
    app.register_blueprint(swaggerui_blueprint)
    # --- End of Swagger Configuration ---

    # Import and register blueprints within app context
    with app.app_context():
        # Import models to ensure they are registered with SQLAlchemy
        from app.models.whatsapp_account import WhatsAppAccount
        from app.models.whatsapp_template import WhatsAppTemplate
        from app.models.whatsapp_message import WhatsAppMessage
        
        # Then import and register blueprints
        from app.controllers.api import api_bp
        app.register_blueprint(api_bp)

    return app