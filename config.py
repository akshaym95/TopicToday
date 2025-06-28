import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class BaseConfig:
    """Base configuration class with common settings"""
    
    # Flask Core Settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dR9#kL5$mN2@pQ7*vB4&hJ8^wF3!tC6'
    DEBUG = False
    TESTING = False
    
    # Database Settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///topic_today.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Set to True to see SQL queries in console
    
    # JWT Settings - Use the same key for both
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'xK8#mP9$vL2@nQ4*hR7&jW3^cF5!bN6'
    JWT_ACCESS_TOKEN_EXPIRES = False  # For development, set to timedelta(hours=1) in production
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_ERROR_MESSAGE_KEY = 'message'
    JWT_ALGORITHM = 'HS256'  # Explicitly set algorithm
    
    # External API Settings
    GNEWS_API_KEY = os.environ.get('GNEWS_API_KEY') or '1234567890'
    GNEWS_BASE_URL = 'https://gnews.io/api/v4'
    GNEWS_MAX_ARTICLES = 5
    GNEWS_LANGUAGE = 'en'
    
    # Application Settings
    APP_NAME = 'TopicToday'
    APP_VERSION = '1.0.0'
    MAX_TOPICS_PER_USER = 10
    DEFAULT_TOPICS = ['technology', 'health', 'sports', 'business']
    VALID_TOPICS = [
        'technology', 'health', 'sports', 'business', 
        'science', 'entertainment', 'politics', 'education'
    ]
    
    # Rate Limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URL = 'memory://'
    RATELIMIT_DEFAULT = '200 per day;50 per hour'
    
    # Caching
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'topic_today.log'
    
    # Security
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Pagination
    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100

class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    LOG_LEVEL = 'DEBUG'
    
    # Development-specific settings
    JWT_ACCESS_TOKEN_EXPIRES = False  # No expiration for development
    CACHE_TYPE = 'null'  # Disable caching in development

class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    
    # Production-specific settings
    SESSION_COOKIE_SECURE = True
    LOG_LEVEL = 'WARNING'
    
    # Use environment variables for sensitive data
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    
    # Only validate production requirements when actually using production config
    def __init__(self):
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY must be set in production")
        if not self.JWT_SECRET_KEY:
            raise ValueError("JWT_SECRET_KEY must be set in production")

class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    JWT_ACCESS_TOKEN_EXPIRES = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name=None):
    """
    Get configuration class based on environment
    
    Args:
        config_name (str, optional): Configuration name. Defaults to None.
        
    Returns:
        class: Configuration class
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    config_class = config.get(config_name, config['default'])
    
    # If it's production config, validate the requirements
    if config_name == 'production':
        config_class()  # This will raise ValueError if requirements not met
    
    return config_class

ZENQUOTES_BASE_URL = 'https://zenquotes.io/api'