from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User
from app import db

# Create namespace for authentication
auth_ns = Namespace('auth', description='Authentication operations')

# Define models for request/response documentation
user_model = auth_ns.model('User', {
    'id': fields.Integer(readonly=True, description='User ID'),
    'username': fields.String(required=True, description='Username'),
    'phone_number': fields.String(required=True, description='Phone number'),
    'preferred_topics': fields.List(fields.String, description='User preferred topics'),
    'created_at': fields.DateTime(readonly=True, description='Account creation date')
})

register_model = auth_ns.model('Register', {
    'username': fields.String(required=True, description='Username', example='john_doe'),
    'phone_number': fields.String(required=True, description='Phone number', example='+1234567890'),
    'password': fields.String(required=True, description='Password', example='securepassword123')
})

login_model = auth_ns.model('Login', {
    'username': fields.String(required=True, description='Username', example='john_doe'),
    'password': fields.String(required=True, description='Password', example='securepassword123')
})

auth_response_model = auth_ns.model('AuthResponse', {
    'message': fields.String(description='Response message'),
    'access_token': fields.String(description='JWT access token'),
    'user': fields.Nested(user_model, description='User information')
})

error_model = auth_ns.model('Error', {
    'error': fields.String(description='Error message')
})

@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(register_model)
    @auth_ns.response(201, 'User registered successfully', auth_response_model)
    @auth_ns.response(400, 'Validation error', error_model)
    @auth_ns.response(500, 'Registration failed', error_model)
    def post(self):
        """Register a new user"""
        data = request.get_json()
        
        # Validate required fields
        if not all(k in data for k in ['username', 'phone_number', 'password']):
            auth_ns.abort(400, 'Missing required fields')
        
        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            auth_ns.abort(400, 'Username already exists')
        
        if User.query.filter_by(phone_number=data['phone_number']).first():
            auth_ns.abort(400, 'Phone number already exists')
        
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
            access_token = create_access_token(identity=user.id)
            
            return {
                'message': 'User registered successfully',
                'access_token': access_token,
                'user': user.to_dict()
            }, 201
            
        except Exception as e:
            db.session.rollback()
            auth_ns.abort(500, 'Registration failed')

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.response(200, 'Login successful', auth_response_model)
    @auth_ns.response(400, 'Missing credentials', error_model)
    @auth_ns.response(401, 'Invalid credentials', error_model)
    def post(self):
        """Login user"""
        data = request.get_json()
        
        if not all(k in data for k in ['username', 'password']):
            auth_ns.abort(400, 'Missing username or password')
        
        # Find user by username
        user = User.query.filter_by(username=data['username']).first()
        
        if user and user.check_password(data['password']):
            # Create JWT token
            access_token = create_access_token(identity=user.id)
            
            return {
                'message': 'Login successful',
                'access_token': access_token,
                'user': user.to_dict()
            }, 200
        else:
            auth_ns.abort(401, 'Invalid username or password')

@auth_ns.route('/profile')
class Profile(Resource):
    @auth_ns.doc(security='apikey')
    @auth_ns.response(200, 'Profile retrieved successfully', user_model)
    @auth_ns.response(401, 'Unauthorized', error_model)
    @auth_ns.response(404, 'User not found', error_model)
    @jwt_required()
    def get(self):
        """Get current user profile"""
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            auth_ns.abort(404, 'User not found')
        
        return user.to_dict(), 200 