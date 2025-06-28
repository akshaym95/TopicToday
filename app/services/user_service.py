from app.models import User
from app import db

class UserService:
    """Service layer for user operations"""

    @staticmethod
    def create_user(data):
        """Create a new user"""
        if not all(k in data for k in ['username', 'phone_number', 'password']):
            return {'error': 'Missing required fields'}, 400

        if User.query.filter_by(username=data['username']).first():
            return {'error': 'Username already exists'}, 400

        if User.query.filter_by(phone_number=data['phone_number']).first():
            return {'error': 'Phone number already exists'}, 400

        user = User(
            username=data['username'],
            phone_number=data['phone_number']
        )
        user.set_password(data['password'])

        try:
            db.session.add(user)
            db.session.commit()
            return user, 201
        except Exception as e:
            db.session.rollback()
            return {'error': 'Registration failed'}, 500

    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        user = User.query.get(int(user_id))
        if not user:
            return {'error': 'User not found'}, 404
        return user, 200

    @staticmethod
    def update_user(user_id, data):
        """Update user info (future use)"""
        user = User.query.get(int(user_id))
        if not user:
            return {'error': 'User not found'}, 404
        # Example: update username or phone_number
        if 'username' in data:
            user.username = data['username']
        if 'phone_number' in data:
            user.phone_number = data['phone_number']
        if 'password' in data:
            user.set_password(data['password'])
        try:
            db.session.commit()
            return user, 200
        except Exception as e:
            db.session.rollback()
            return {'error': 'Update failed'}, 500 