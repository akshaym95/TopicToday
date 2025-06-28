from flask import jsonify
from app.models import User
from app import db
from flask_jwt_extended import create_access_token

class AuthService:
    """Service layer for authentication operations"""
    
    @staticmethod
    def register_user(data):
        """Register a new user"""
        # Validate required fields
        if not all(k in data for k in ['username', 'phone_number', 'password']):
            return {'error': 'Missing required fields'}, 400
        
        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            return {'error': 'Username already exists'}, 400
        
        if User.query.filter_by(phone_number=data['phone_number']).first():
            return {'error': 'Phone number already exists'}, 400
        
        # Create new user
        user = User(
            username=data['username'],
            phone_number=data['phone_number']
        )
        user.set_password(data['password'])
        
        try:
            db.session.add(user)
            db.session.commit()
            
            # Create JWT token
            access_token = create_access_token(identity=str(user.id))
            
            return {
                'message': 'User registered successfully',
                'access_token': access_token,
                'user': user.to_dict()
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': 'Registration failed'}, 500
    
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
            return {'error': 'Invalid username or password'}, 401
    
    @staticmethod
    def get_user_profile(user_id):
        """Get user profile by ID"""
        user = User.query.get(int(user_id))
        
        if not user:
            return {'error': 'User not found'}, 404
        
        return user.to_dict(), 200 