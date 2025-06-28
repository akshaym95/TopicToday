from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User
from app.services.news_service import NewsService
from app.services.quotes_service import QuotesService
from app import db

# Create namespace for dashboard operations
dashboard_ns = Namespace('dashboard', description='Dashboard operations')

# Define models for request/response documentation
news_model = dashboard_ns.model('News', {
    'title': fields.String(description='News title'),
    'description': fields.String(description='News description'),
    'url': fields.String(description='News URL'),
    'image': fields.String(description='News image URL'),
    'publishedAt': fields.String(description='Publication date'),
    'source': fields.String(description='News source'),
    'topic': fields.String(description='News topic')
})

quote_model = dashboard_ns.model('Quote', {
    'quote': fields.String(description='Quote text'),
    'author': fields.String(description='Quote author'),
    'source': fields.String(description='Quote source')
})

feed_model = dashboard_ns.model('Feed', {
    'news': fields.List(fields.Nested(news_model), description='News articles'),
    'quotes': fields.List(fields.Nested(quote_model), description='Motivational quotes'),
    'user_topics': fields.List(fields.String, description='User preferred topics')
})

preferences_model = dashboard_ns.model('Preferences', {
    'topics': fields.List(fields.String, required=True, description='List of preferred topics', example=['technology', 'health', 'sports'])
})

preferences_response_model = dashboard_ns.model('PreferencesResponse', {
    'message': fields.String(description='Response message'),
    'topics': fields.List(fields.String, description='Updated topics')
})

error_model = dashboard_ns.model('Error', {
    'error': fields.String(description='Error message')
})

@dashboard_ns.route('/preferences')
class Preferences(Resource):
    @dashboard_ns.doc(security='Bearer Auth')
    @dashboard_ns.expect(preferences_model)
    @dashboard_ns.response(200, 'Preferences updated successfully', preferences_response_model)
    @dashboard_ns.response(400, 'Validation error', error_model)
    @dashboard_ns.response(401, 'Unauthorized', error_model)
    @dashboard_ns.response(404, 'User not found', error_model)
    @dashboard_ns.response(500, 'Update failed', error_model)
    @jwt_required()
    def put(self):
        """Update user's preferred topics"""
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            dashboard_ns.abort(404, 'User not found')
        
        data = request.get_json()
        
        if 'topics' not in data:
            dashboard_ns.abort(400, 'Topics field is required')
        
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
            dashboard_ns.abort(500, 'Failed to update preferences')

@dashboard_ns.route('/feed')
class Feed(Resource):
    @dashboard_ns.doc(security='Bearer Auth')
    @dashboard_ns.response(200, 'Feed retrieved successfully', feed_model)
    @dashboard_ns.response(401, 'Unauthorized', error_model)
    @dashboard_ns.response(404, 'User not found', error_model)
    @jwt_required()
    def get(self):
        """Get personalized feed with news and quotes"""
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            dashboard_ns.abort(404, 'User not found')
        
        topics = user.get_topics()
        
        # Initialize services
        news_service = NewsService()
        quotes_service = QuotesService()
        
        feed = {
            'news': [],
            'quotes': [],
            'user_topics': topics
        }
        
        # Get news for each topic
        for topic in topics:
            try:
                news = news_service.get_news_by_topic(topic)
                feed['news'].extend(news)
            except Exception as e:
                print(f"Error fetching news for {topic}: {e}")
        
        # Get motivational quotes
        try:
            quotes = quotes_service.get_random_quotes(3)
            feed['quotes'] = quotes
        except Exception as e:
            print(f"Error fetching quotes: {e}")
        
        return feed, 200 