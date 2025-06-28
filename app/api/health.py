from flask_restx import Namespace, Resource, fields

# Create namespace for health checks
health_ns = Namespace('health', description='Health check operations')

health_model = health_ns.model('Health', {
    'status': fields.String(description='Service status'),
    'version': fields.String(description='API version'),
    'timestamp': fields.String(description='Current timestamp')
})

@health_ns.route('')
class Health(Resource):
    @health_ns.response(200, 'Service is healthy', health_model)
    def get(self):
        """Health check endpoint"""
        from datetime import datetime
        return {
            'status': 'healthy',
            'version': '1.0.0',
            'timestamp': datetime.utcnow().isoformat()
        }, 200 