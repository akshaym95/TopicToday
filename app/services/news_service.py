import requests
import os
from typing import List, Dict
from config import GNEWS_BASE_URL, GNEWS_API_KEY

class NewsService:
    """Service for fetching news from GNews API"""
    
    def __init__(self):
        self.api_key = GNEWS_API_KEY
        self.base_url = GNEWS_BASE_URL
    
    def get_news_by_topic(self, topic: str) -> List[Dict]:
        """Fetch news articles for a specific topic"""
        if not self.api_key:
            print("no api key")
            # Return mock data if no API key
            return self._get_mock_news(topic)
        
        try:
            url = f"{self.base_url}/search"
            params = {
                'q': topic,
                'token': self.api_key,
                'lang': 'en',
                'country': 'in',
                'max': 3,
                'sortby': 'publishedAt'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            articles = data.get('articles', [])
            
            # Format articles for our app
            formatted_articles = []
            for article in articles:
                formatted_articles.append({
                    'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'url': article.get('url', ''),
                    'image': article.get('image', ''),
                    'publishedAt': article.get('publishedAt', ''),
                    'source': article.get('source', {}).get('name', ''),
                    'topic': topic
                })
            
            return formatted_articles
            
        except requests.RequestException as e:
            print(f"Error fetching news for {topic}: {e}")
            #return self._get_mock_news(topic)
            return []
    
    def _get_mock_news(self, topic: str) -> List[Dict]:
        """Return mock news data when API is unavailable"""
        mock_articles = {
            'technology': [
                {
                    'title': f'Latest in {topic.title()}: AI Breakthrough',
                    'description': f'Exciting developments in {topic} technology',
                    'url': 'https://example.com',
                    'image': 'https://via.placeholder.com/300x200',
                    'publishedAt': '2024-01-01T00:00:00Z',
                    'source': 'Tech News',
                    'topic': topic
                }
            ],
            'health': [
                {
                    'title': f'Health Update: New {topic.title()} Research',
                    'description': f'Important findings in {topic} health',
                    'url': 'https://example.com',
                    'image': 'https://via.placeholder.com/300x200',
                    'publishedAt': '2024-01-01T00:00:00Z',
                    'source': 'Health News',
                    'topic': topic
                }
            ]
        }
        
        return mock_articles.get(topic, [
            {
                'title': f'{topic.title()} News',
                'description': f'Latest updates in {topic}',
                'url': 'https://example.com',
                'image': 'https://via.placeholder.com/300x200',
                'publishedAt': '2024-01-01T00:00:00Z',
                'source': 'News Source',
                'topic': topic
            }
        ]) 