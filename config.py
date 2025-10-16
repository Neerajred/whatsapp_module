# File: config.py
import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-me'
    JWT_ACCESS_TOKEN_EXPIRES = False
    
    # WhatsApp API Configuration
    META_API_BASE_URL = os.environ.get('META_API_BASE_URL', 'https://graph.facebook.com')
    META_API_VERSION = os.environ.get('META_API_VERSION', 'v23.0')
    
    # Media upload configuration
    MEDIA_UPLOAD_FOLDER = os.environ.get('MEDIA_UPLOAD_FOLDER', 'media_uploads')
    MAX_MEDIA_SIZE = int(os.environ.get('MAX_MEDIA_SIZE', 16 * 1024 * 1024))

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    # Default to PostgreSQL with common default credentials
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:password@localhost:5432/whatsapp_module'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///:memory:'

class ProductionConfig(Config):
    """Production configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}