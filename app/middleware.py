from flask import request, g
import logging
import time
from datetime import datetime

def setup_request_logging(app):
    """Setup request logging middleware"""
    
    @app.before_request
    def before_request():
        g.start_time = time.time()
        g.request_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{id(request)}"
        
        # Log request details
        app.logger.info(
            f"Request {g.request_id}: {request.method} {request.path} "
            f"from {request.remote_addr} - User-Agent: {request.headers.get('User-Agent', 'Unknown')}"
        )
        
        # Log request body for POST/PUT requests
        if request.method in ['POST', 'PUT'] and request.is_json:
            app.logger.debug(f"Request {g.request_id} body: {request.get_json()}")
    
    @app.after_request
    def after_request(response):
        # Calculate request duration
        duration = time.time() - g.start_time
        
        # Log response details
        app.logger.info(
            f"Response {g.request_id}: {response.status_code} "
            f"({duration:.3f}s) - {request.method} {request.path}"
        )
        
        # Log response body for errors
        if response.status_code >= 400:
            app.logger.error(
                f"Error {g.request_id}: {response.status_code} - "
                f"Response: {response.get_data(as_text=True)}"
            )
        
        return response
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
        return {
            'error': 'Internal server error',
            'message': 'An unexpected error occurred.'
        }, 500 