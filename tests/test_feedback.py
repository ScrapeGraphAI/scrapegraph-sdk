import unittest
from unittest.mock import patch
from scrapegraphaiapisdk.feedback import feedback

class TestFeedback(unittest.TestCase):
    
    @patch('scrapegraphaiapisdk.feedback.requests.post')
    def test_feedback_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = '{"status": "success"}'
        response = feedback("test_api_key", "Great service!")
        self.assertEqual(response, '{"status": "success"}')

    @patch('scrapegraphaiapisdk.feedback.requests.post')
    def test_feedback_http_error(self, mock_post):
        mock_post.side_effect = requests.exceptions.HTTPError
        response = feedback("test_api_key", "Great service!")
        self.assertIn("HTTP error occurred", response)

# ... additional tests can be added here ...

if __name__ == '__main__':
    unittest.main() 