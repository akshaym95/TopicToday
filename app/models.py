from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

class User(db.Model):
    """User model for authentication and preferences"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone_number = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Store topics as JSON string
    preferred_topics = db.Column(db.Text, default='[]')
    
    def set_password(self, password):
        """Hash password before storing"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def get_topics(self):
        """Get preferred topics as list"""
        return json.loads(self.preferred_topics)
    
    def set_topics(self, topics):
        """Set preferred topics from list"""
        self.preferred_topics = json.dumps(topics)
    
    def to_dict(self):
        """Convert user to dictionary (exclude password)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone_number': self.phone_number,
            'preferred_topics': self.get_topics(),
            'created_at': self.created_at.isoformat()
        } 