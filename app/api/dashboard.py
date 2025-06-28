from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User
from app.services.news_service import NewsService
from app.services.quotes_service import QuotesService
from app.services.user_service import UserService
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

error_model = dashboard_ns.model('Error', {
    'error': fields.String(description='Error message')
})

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
        user_or_error, status_code = UserService.get_user_by_id(current_user_id)
        if status_code != 200:
            dashboard_ns.abort(status_code, user_or_error.get('error', 'User not found'))
        user = user_or_error
        
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