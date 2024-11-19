import unittest
import requests
from unittest.mock import patch, Mock
from scrapegraph_py.credits import credits
from scrapegraph_py.client import ScrapeGraphClient

class TestCredits(unittest.TestCase):
    
    def setUp(self):
        self.client = ScrapeGraphClient("test_api_key")
    
    @patch('scrapegraph_py.credits.requests.get')
    def test_credits_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = '{"credits": 100}'
        response = credits(self.client)
        self.assertEqual(response, '{"credits": 100}')

    @patch('scrapegraph_py.credits.requests.get')
    def test_credits_http_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.HTTPError
        response = credits(self.client)
        self.assertIn("HTTP error occurred", response)

if __name__ == '__main__':
    unittest.main() 