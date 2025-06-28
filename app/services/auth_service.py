from flask import jsonify
from app.models import User
from app import db
from flask_jwt_extended import create_access_token
from app.services.user_service import UserService

class AuthService:
    """Service layer for authentication operations"""
    
    @staticmethod
    def register_user(data):
        """Register a new user (delegates to UserService)"""
        user_or_error, status_code = UserService.create_user(data)
        if status_code != 201:
            return user_or_error, status_code
        user = user_or_error
        access_token = create_access_token(identity=str(user.id))
        return {
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': user.to_dict()
        }, 201
    
    @staticmethod
    def login_user(data):
        """Login user"""
        if not all(k in data for k in ['username', 'password']):
            return {'error': 'Missing username or password'}, 400
        
        # Find user by username
        user = User.query.filter_by(username=data['username']).first()
        
        if user and user.check_password(data['password']):
            # Create JWT token
            access_token = create_access_token(identity=str(user.id))
            
            return {
                'message': 'Login successful',
                'access_token': access_token,
                'user': user.to_dict()
            }, 200
        else:
            return {'error': 'Invalid credentials'}, 401
    
    @staticmethod
    def get_user_profile(user_id):
        """Get user profile by ID (delegates to UserService)"""
        user_or_error, status_code = UserService.get_user_by_id(user_id)
        if status_code != 200:
            return user_or_error, status_code
        user = user_or_error
        return user.to_dict(), 200 