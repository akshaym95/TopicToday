from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth_service import AuthService

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
        result, status_code = AuthService.register_user(data)
        
        if status_code >= 400:
            auth_ns.abort(status_code, result['error'])
        
        return result, status_code

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.response(200, 'Login successful', auth_response_model)
    @auth_ns.response(400, 'Missing credentials', error_model)
    @auth_ns.response(401, 'Invalid credentials', error_model)
    def post(self):
        """Login user"""
        data = request.get_json()
        result, status_code = AuthService.login_user(data)
        
        if status_code >= 400:
            auth_ns.abort(status_code, result['error'])
        
        return result, status_code 