from flask import Blueprint
from flask_restx import Api

# Create API blueprint
bp = Blueprint('api', __name__)

# Initialize Flask-RESTX API with proper security configuration
api = Api(
    bp,
    title='TopicToday API',
    version='1.0.0',
    description='A Flask-based REST API that provides personalized news feeds and motivational quotes based on user preferences',
    doc='/docs/',
    authorizations={
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "Type 'Bearer <JWT>' where JWT is the token"
        }
    },
    security='Bearer Auth',  # Set default security
    contact='Akshay M',
    contact_email='akshaym95@gmail.com',
    contact_url='https://github.com/akshaym95/topic-today',
    license='MIT',
    license_url='https://opensource.org/licenses/MIT'
)

# Import namespaces after API initialization
from app.api.auth import auth_ns
from app.api.dashboard import dashboard_ns
from app.api.health import health_ns
from app.api.user import user_ns

# Add namespaces to API
api.add_namespace(health_ns, path='/health')
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(dashboard_ns, path='/dashboard')
api.add_namespace(user_ns, path='/user') 