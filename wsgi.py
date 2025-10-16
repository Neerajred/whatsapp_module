# File: wsgi.py
import os
import sys
from dotenv import load_dotenv

# --- The Definitive Fix ---
# 1. Add the project's root directory to the Python path.
# This ensures that modules like 'config' and 'app' can be found.
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

# 2. Explicitly load the .env file from the project root.
# This makes sure environment variables are set before the app is created.
load_dotenv(os.path.join(project_root, '.env'))
# --- End of Fix ---

# Now that the environment and path are correctly set, we can import the factory.
from app import create_app

# Create the application instance using the factory
config_name = os.environ.get('FLASK_CONFIG', 'development')
app = create_app(config_name)


if __name__ == '__main__':
    # This allows running the app directly with 'python wsgi.py'
    app.run(debug=True)