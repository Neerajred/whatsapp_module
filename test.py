# File: simple_test.py
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

def test_config():
    """Test if configuration is loaded correctly"""
    print("=== Testing Configuration ===")
    
    # Check environment variables
    print("Environment Variables:")
    print(f"FLASK_CONFIG: {os.environ.get('FLASK_CONFIG')}")
    print(f"DATABASE_URL: {os.environ.get('DATABASE_URL')}")
    
    # Test config import
    try:
        from config import config
        print("\nConfig loaded successfully:")
        print(f"Debug mode: {config['development'].DEBUG}")
        print(f"Database URI: {config['development'].SQLALCHEMY_DATABASE_URI}")
        return True
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def test_database():
    """Test database connection"""
    print("\n=== Testing Database ===")
    
    try:
        from app import create_app, db
        
        app = create_app('development')
        
        with app.app_context():
            # Test connection
            db.engine.connect()
            print("✓ Database connection successful")
            
            # Create tables
            db.create_all()
            print("✓ Tables created successfully")
            
            return True
            
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

if __name__ == "__main__":
    if test_config():
        test_database()