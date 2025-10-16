# File: setup_database.py
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

def setup_postgresql():
    """Helper function to setup PostgreSQL database"""
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    
    # Get database connection parameters from environment
    db_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/postgres')
    
    # Extract components from URL
    if db_url.startswith('postgresql://'):
        db_url = db_url.replace('postgresql://', '')
    
    user_pass, host_port_db = db_url.split('@')
    username, password = user_pass.split(':')
    host_port, database = host_port_db.split('/')
    host, port = host_port.split(':')
    
    print(f"Connecting to PostgreSQL: {username}@{host}:{port}")
    
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database='postgres'  # Connect to default postgres database
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (database,))
        exists = cursor.fetchone()
        
        if not exists:
            print(f"Creating database: {database}")
            cursor.execute(f'CREATE DATABASE {database}')
            print("✓ Database created successfully")
        else:
            print(f"✓ Database {database} already exists")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error setting up PostgreSQL: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure PostgreSQL is running: sudo service postgresql start")
        print("2. Check your credentials in the .env file")
        print("3. Try connecting manually: psql -U postgres -h localhost")
        return False

def main():
    """Main setup function"""
    print("=== WhatsApp Module Database Setup ===")
    
    # Setup PostgreSQL database
    if not setup_postgresql():
        return
    
    # Now test the Flask application
    try:
        from app import create_app, db
        
        app = create_app('development')
        
        with app.app_context():
            print("\nCreating database tables...")
            db.create_all()
            print("✓ Tables created successfully")
            
            # Test with a simple query
            from app.models.whatsapp_account import WhatsAppAccount
            count = WhatsAppAccount.query.count()
            print(f"✓ Database is working. Current accounts: {count}")
            
            print("\nSetup completed successfully!")
            print("\nNext steps:")
            print("1. Run: flask db init (if you want migrations)")
            print("2. Run: flask run (to start the server)")
            print("3. Visit: http://localhost:5000/api/docs")
            
    except Exception as e:
        print(f"Error during Flask setup: {e}")

if __name__ == "__main__":
    main()