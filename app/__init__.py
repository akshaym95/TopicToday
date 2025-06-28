from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import get_config
import logging
import os
from datetime import datetime
from app.middleware import setup_request_logging

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_name=None):
    """Application Factory Pattern"""
    app = Flask(__name__)
    
    # Load configuration
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    
    # Setup logging
    setup_logging(app)
    
    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    
    # Setup JWT error handlers
    setup_jwt_error_handlers(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Setup request logging
    setup_request_logging(app)
    
    return app

def setup_logging(app):
    """Setup comprehensive logging"""
    if not app.debug and not app.testing:
        # Create logs directory if it doesn't exist
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Setup file handler
        file_handler = logging.FileHandler(f'{log_dir}/topic_today.log')
        file_handler.setLevel(logging.INFO)
        
        # Setup formatter
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        file_handler.setFormatter(formatter)
        
        # Add handler to app logger
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('TopicToday startup')
    
    # Always log to console in development
    if app.debug:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        app.logger.addHandler(console_handler)
        app.logger.setLevel(logging.DEBUG)

def setup_jwt_error_handlers(app):
    """Setup JWT error handlers for better error messages"""
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        app.logger.warning(f"Expired token attempt: {jwt_payload}")
        return {
            'error': 'Token has expired',
            'message': 'The token has expired. Please login again.'
        }, 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        app.logger.warning(f"Invalid token attempt: {error}")
        return {
            'error': 'Invalid token',
            'message': 'The token is invalid. Please provide a valid token.'
        }, 422
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        app.logger.warning(f"Missing token attempt: {error}")
        return {
            'error': 'Missing token',
            'message': 'Authorization header is missing. Please provide a valid token.'
        }, 401
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        app.logger.warning(f"Non-fresh token attempt: {jwt_payload}")
        return {
            'error': 'Token not fresh',
            'message': 'A fresh token is required for this operation.'
        }, 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        app.logger.warning(f"Revoked token attempt: {jwt_payload}")
        return {
            'error': 'Token revoked',
            'message': 'The token has been revoked.'
        }, 401

def register_blueprints(app):
    """Register application blueprints"""
    # Register API documentation (Flask-RESTX)
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api') 