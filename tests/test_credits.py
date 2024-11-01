import unittest
from unittest.mock import patch
from scrapegraphaiapisdk.credits import credits

class TestCredits(unittest.TestCase):
    
    @patch('scrapegraphaiapisdk.credits.requests.get')
    def test_credits_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = '{"credits": 100}'
        response = credits("test_api_key")
        self.assertEqual(response, '{"credits": 100}')

    @patch('scrapegraphaiapisdk.credits.requests.get')
    def test_credits_http_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.HTTPError
        response = credits("test_api_key")
        self.assertIn("HTTP error occurred", response)

if __name__ == '__main__':
    unittest.main() 