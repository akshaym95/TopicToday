from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.auth import bp
from app.services.auth_service import AuthService

@bp.route('/register', methods=['POST'])
def register():
    """User registration endpoint"""
    data = request.get_json()
    result, status_code = AuthService.register_user(data)
    return jsonify(result), status_code

@bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    data = request.get_json()
    result, status_code = AuthService.login_user(data)
    return jsonify(result), status_code

@bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    """Get current user profile"""
    current_user_id = get_jwt_identity()
    result, status_code = AuthService.get_user_profile(current_user_id)
    return jsonify(result), status_code 