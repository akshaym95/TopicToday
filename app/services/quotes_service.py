import requests
import os
from typing import List, Dict

class QuotesService:
    """Service for fetching motivational quotes from ZenQuotes API"""
    
    def __init__(self):
        self.base_url = 'https://zenquotes.io/api'
    
    def get_random_quotes(self, count: int = 3) -> List[Dict]:
        """Fetch random motivational quotes"""
        try:
            url = f"{self.base_url}/random"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # ZenQuotes returns a list of quotes
            quotes = []
            for quote_data in data[:count]:
                quotes.append({
                    'quote': quote_data.get('q', ''),
                    'author': quote_data.get('a', 'Unknown'),
                    'source': 'ZenQuotes'
                })
            
            return quotes
            
        except requests.RequestException as e:
            print(f"Error fetching quotes: {e}")
            return self._get_mock_quotes(count)
    
    def _get_mock_quotes(self, count: int) -> List[Dict]:
        """Return mock quotes when API is unavailable"""
        mock_quotes = [
            {
                'quote': 'The only way to do great work is to love what you do.',
                'author': 'Steve Jobs',
                'source': 'Mock Quotes'
            },
            {
                'quote': 'Success is not final, failure is not fatal: it is the courage to continue that counts.',
                'author': 'Winston Churchill',
                'source': 'Mock Quotes'
            },
            {
                'quote': 'The future belongs to those who believe in the beauty of their dreams.',
                'author': 'Eleanor Roosevelt',
                'source': 'Mock Quotes'
            }
        ]
        
        return mock_quotes[:count] 