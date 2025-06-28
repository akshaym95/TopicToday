import requests
from typing import List, Dict
from config import ZENQUOTES_BASE_URL

class QuotesService:
    """Service for fetching motivational quotes from ZenQuotes API"""
    
    def __init__(self):
        self.base_url = ZENQUOTES_BASE_URL
    
    def get_qoute_of_the_day(self) -> List[Dict]:
        """Fetch motivational quotes of the day"""
        try:
            url = f"{self.base_url}/today"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # ZenQuotes returns a list of quotes
            quotes = []
            qoute = data[0]
            quotes.append({
                    'quote': qoute.get('q', ''),
                    'author': qoute.get('a', 'Unknown'),
                    'source': 'ZenQuotes'
                })
            
            return quotes
            
        except requests.RequestException as e:
            print(f"Error fetching quotes: {e}")
            return self._get_mock_quotes()
    
    def _get_mock_quotes(self) -> List[Dict]:
        """Return mock quotes when API is unavailable"""
        mock_quotes = [
            {
                'quote': 'The only way to do great work is to love what you do.',
                'author': 'Steve Jobs',
                'source': 'Mock Quotes'
            }
        ]
        
        return mock_quotes