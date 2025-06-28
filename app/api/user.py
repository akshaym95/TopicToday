from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService
from app.models import User
from app import db

# Create namespace for user operations
user_ns = Namespace('user', description='User operations')

# Define models for request/response documentation
preferences_model = user_ns.model('Preferences', {
    'topics': fields.List(fields.String, required=True, description='List of preferred topics', example=['technology', 'health', 'sports'])
})

preferences_response_model = user_ns.model('PreferencesResponse', {
    'message': fields.String(description='Response message'),
    'topics': fields.List(fields.String, description='Updated topics')
})

update_profile_model = user_ns.model('UpdateProfile', {
    'username': fields.String(description='New username', example='new_username'),
    'phone_number': fields.String(description='New phone number', example='+1234567890'),
    'password': fields.String(description='New password', example='newpassword123')
})

user_profile_model = user_ns.model('UserProfile', {
    'id': fields.Integer(readonly=True, description='User ID'),
    'username': fields.String(description='Username'),
    'phone_number': fields.String(description='Phone number'),
    'preferred_topics': fields.List(fields.String, description='User preferred topics'),
    'created_at': fields.DateTime(readonly=True, description='Account creation date')
})

profile_response_model = user_ns.model('ProfileResponse', {
    'message': fields.String(description='Response message'),
    'user': fields.Nested(user_profile_model, description='Updated user information')
})

error_model = user_ns.model('Error', {
    'error': fields.String(description='Error message')
})

@user_ns.route('/profile')
class UserProfile(Resource):
    @user_ns.doc(security='Bearer Auth')
    @user_ns.response(200, 'Profile retrieved successfully', user_profile_model)
    @user_ns.response(401, 'Unauthorized', error_model)
    @user_ns.response(404, 'User not found', error_model)
    @jwt_required()
    def get(self):
        """Get current user profile"""
        current_user_id = get_jwt_identity()
        user_or_error, status_code = UserService.get_user_by_id(current_user_id)
        if status_code != 200:
            user_ns.abort(status_code, user_or_error.get('error', 'User not found'))
        user = user_or_error
        return user.to_dict(), 200

    @user_ns.doc(security='Bearer Auth')
    @user_ns.expect(update_profile_model)
    @user_ns.response(200, 'Profile updated successfully', profile_response_model)
    @user_ns.response(400, 'Validation error', error_model)
    @user_ns.response(401, 'Unauthorized', error_model)
    @user_ns.response(404, 'User not found', error_model)
    @user_ns.response(409, 'Username or phone number already exists', error_model)
    @user_ns.response(500, 'Update failed', error_model)
    @jwt_required()
    def put(self):
        """Update user profile information"""
        current_user_id = get_jwt_identity()
        user_or_error, status_code = UserService.get_user_by_id(current_user_id)
        if status_code != 200:
            user_ns.abort(status_code, user_or_error.get('error', 'User not found'))
        user = user_or_error

        data = request.get_json()
        if not data:
            user_ns.abort(400, 'No data provided for update')

        # Check for duplicate username if username is being updated
        if 'username' in data and data['username'] != user.username:
            existing_user = User.query.filter_by(username=data['username']).first()
            if existing_user:
                user_ns.abort(409, 'Username already exists')

        # Check for duplicate phone number if phone_number is being updated
        if 'phone_number' in data and data['phone_number'] != user.phone_number:
            existing_user = User.query.filter_by(phone_number=data['phone_number']).first()
            if existing_user:
                user_ns.abort(409, 'Phone number already exists')

        # Update user fields
        if 'username' in data:
            user.username = data['username']
        if 'phone_number' in data:
            user.phone_number = data['phone_number']
        if 'password' in data:
            user.set_password(data['password'])

        try:
            db.session.commit()
            return {
                'message': 'Profile updated successfully',
                'user': user.to_dict()
            }, 200
        except Exception as e:
            db.session.rollback()
            user_ns.abort(500, 'Failed to update profile')

@user_ns.route('/preferences')
class UserPreferences(Resource):
    @user_ns.doc(security='Bearer Auth')
    @user_ns.response(200, 'Preferences retrieved successfully', user_profile_model)
    @user_ns.response(401, 'Unauthorized', error_model)
    @user_ns.response(404, 'User not found', error_model)
    @jwt_required()
    def get(self):
        """Get current user preferences"""
        current_user_id = get_jwt_identity()
        user_or_error, status_code = UserService.get_user_by_id(current_user_id)
        if status_code != 200:
            user_ns.abort(status_code, user_or_error.get('error', 'User not found'))
        user = user_or_error
        return user.to_dict(), 200

    @user_ns.doc(security='Bearer Auth')
    @user_ns.expect(preferences_model)
    @user_ns.response(200, 'Preferences updated successfully', preferences_response_model)
    @user_ns.response(400, 'Validation error', error_model)
    @user_ns.response(401, 'Unauthorized', error_model)
    @user_ns.response(404, 'User not found', error_model)
    @user_ns.response(500, 'Update failed', error_model)
    @jwt_required()
    def put(self):
        """Update user's preferred topics"""
        current_user_id = get_jwt_identity()
        user_or_error, status_code = UserService.get_user_by_id(current_user_id)
        if status_code != 200:
            user_ns.abort(status_code, user_or_error.get('error', 'User not found'))
        user = user_or_error

        data = request.get_json()
        if 'topics' not in data:
            user_ns.abort(400, 'Topics field is required')

        # Validate topics
        valid_topics = ['technology', 'health', 'sports', 'business', 'science', 'entertainment']
        topics = [topic for topic in data['topics'] if topic in valid_topics]

        user.set_topics(topics)
        try:
            db.session.commit()
            return {
                'message': 'Preferences updated successfully',
                'topics': user.get_topics()
            }, 200
        except Exception as e:
            db.session.rollback()
            user_ns.abort(500, 'Failed to update preferences') 