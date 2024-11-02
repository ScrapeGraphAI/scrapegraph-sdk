import unittest
from unittest.mock import patch
from scrapegraphaiapisdk.feedback import feedback
import requests

class TestFeedback(unittest.TestCase):
    
    @patch('scrapegraphaiapisdk.feedback.requests.post')
    def test_feedback_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = '{"status": "success"}'
        response = feedback("test_api_key", "3fa85f64-5717-4562-b3fc-2c963f66afa6", 5, "Great service!")
        self.assertEqual(response, '{"status": "success"}')

    @patch('scrapegraphaiapisdk.feedback.requests.post')
    def test_feedback_http_error(self, mock_post):
        mock_post.side_effect = requests.exceptions.HTTPError
        response = feedback("test_api_key", "3fa85f64-5717-4562-b3fc-2c963f66afa6", 5, "Great service!")
        self.assertIn("HTTP error occurred", response)

if __name__ == '__main__':
    unittest.main() 