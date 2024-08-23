import unittest
from unittest.mock import patch, Mock
import os
from backend.src.fetch_news_topic import fetch_top_news_topic

class TestFetchTopNewsTopic(unittest.TestCase):
    
    @patch('backend.src.fetch_news_topic.requests.get')
    def test_api_key_missing(self, mock_get):
        # Temporarily remove the NEWS_API_KEY environment variable
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(Exception) as context:
                fetch_top_news_topic('New York')
            self.assertIn("API key not found", str(context.exception))

    @patch('backend.src.fetch_news_topic.requests.get')
    def test_successful_response(self, mock_get):
        # Set the environment variable for the API key
        with patch.dict(os.environ, {'NEWS_API_KEY': 'dummy_key'}):
            # Mock the response from the API
            mock_response = Mock()
            mock_response.json.return_value = {
                'status': 'ok',
                'articles': [
                    {'title': 'Headline 1'},
                    {'title': 'Headline 2'},
                    {'title': 'Headline 3'},
                    {'title': 'Headline 4'},
                    {'title': 'Headline 5'}
                ]
            }
            mock_get.return_value = mock_response
            
            # Call the function
            headlines = fetch_top_news_topic('New York')
            
            # Assert the correct output
            self.assertEqual(headlines, ['Headline 1', 'Headline 2', 'Headline 3', 'Headline 4', 'Headline 5'])

    @patch('backend.src.fetch_news_topic.requests.get')
    def test_api_failure_response(self, mock_get):
        # Set the environment variable for the API key
        with patch.dict(os.environ, {'NEWS_API_KEY': 'dummy_key'}):
            # Mock a failed response from the API
            mock_response = Mock()
            mock_response.json.return_value = {'status': 'error'}
            mock_get.return_value = mock_response
            
            # Assert that an exception is raised
            with self.assertRaises(Exception) as context:
                fetch_top_news_topic('New York')
            self.assertIn("Failed to fetch news topics", str(context.exception))

