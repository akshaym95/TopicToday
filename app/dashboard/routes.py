from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.dashboard import bp
from app.models import User
from app.services.news_service import NewsService
from app.services.quotes_service import QuotesService
from app import db

@bp.route('/preferences', methods=['PUT'])
@jwt_required()
def update_preferences():
    """Update user's preferred topics"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    if 'topics' not in data:
        return jsonify({'error': 'Topics field is required'}), 400
    
    # Validate topics (you can add more validation here)
    valid_topics = ['technology', 'health', 'sports', 'business', 'science', 'entertainment']
    topics = [topic for topic in data['topics'] if topic in valid_topics]
    
    user.set_topics(topics)
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Preferences updated successfully',
            'topics': user.get_topics()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update preferences'}), 500

@bp.route('/feed', methods=['GET'])
@jwt_required()
def get_feed():
    """Get personalized feed with news and quotes"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
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
            # Log error but continue with other topics
            print(f"Error fetching news for {topic}: {e}")
    
    # Get motivational quotes
    try:
        quotes = quotes_service.get_random_quotes(3)
        feed['quotes'] = quotes
    except Exception as e:
        print(f"Error fetching quotes: {e}")
    
    return jsonify(feed), 200 