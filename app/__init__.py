# # File: app/__init__.py
# import os
# import sys
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_jwt_extended import JWTManager
# from flask_cors import CORS
# from flask_swagger_ui import get_swaggerui_blueprint
# from flask import send_from_directory

# # Add the project's root directory to the Python path.
# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# if project_root not in sys.path:
#     sys.path.insert(0, project_root)

# # Now, this import will work reliably.
# from config import config

# # Initialize extensions globally, but without attaching to an app yet.
# db = SQLAlchemy()
# migrate = Migrate()
# jwt = JWTManager()
# cors = CORS()


# def create_app(config_name=None):
#     """Application factory function."""
#     app = Flask(__name__)

#     if config_name is None:
#         config_name = os.environ.get('FLASK_CONFIG', 'default')

#     config_object = config.get(config_name, config['default'])
#     app.config.from_object(config_object)

#     # Initialize extensions with the app instance
#     db.init_app(app)
#     migrate.init_app(app, db)
#     jwt.init_app(app)
#     cors.init_app(app)
    
#     # --- Swagger UI Configuration ---
#     SWAGGER_URL = '/api/docs'
#     API_URL = '/static/swagger.json'

#     @app.route('/static/<path:path>')
#     def send_static(path):
#         return send_from_directory('static', path)

#     swaggerui_blueprint = get_swaggerui_blueprint(
#         SWAGGER_URL,
#         API_URL,
#         config={'app_name': "WhatsApp API Module"}
#     )
#     app.register_blueprint(swaggerui_blueprint)
#     # --- End of Swagger Configuration ---

#     # Move the blueprint and model imports inside the factory.
#     # This ensures they are only imported once, within the application's context.
#     with app.app_context():
#         from .controllers.api import api_bp
#         from . import models

#         app.register_blueprint(api_bp)

#     return app

# File: app/__init__.py
import os
import sys
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

# Add the project's root directory to the Python path.
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

    # Move the blueprint and model imports inside the factory to prevent errors.
    with app.app_context():
        from .controllers.api import api_bp
        from . import models

        app.register_blueprint(api_bp)

    return app