import unittest
from unittest.mock import patch
import os
from dotenv import load_dotenv
from scrapegraph_py.feedback import feedback
from scrapegraph_py.client import ScrapeGraphClient
import requests

class TestFeedback(unittest.TestCase):
    
    def setUp(self):
        # Load environment variables from .env file
        load_dotenv()
        self.api_key = os.getenv('SCRAPEGRAPH_API_KEY', 'test_api_key')
        self.client = ScrapeGraphClient(self.api_key)
    
    @patch('scrapegraph_py.feedback.requests.post')
    def test_feedback_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = '{"status": "success"}'
        response = feedback(
            self.client,
            "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            5,
            "Great service!"
        )
        self.assertEqual(response, '{"status": "success"}')

    @patch('scrapegraph_py.feedback.requests.post')
    def test_feedback_http_error(self, mock_post):
        mock_post.side_effect = requests.exceptions.HTTPError
        response = feedback(
            self.client,
            "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            5,
            "Great service!"
        )
        self.assertIn("HTTP error occurred", response)

if __name__ == '__main__':
    unittest.main() 