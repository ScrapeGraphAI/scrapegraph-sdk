import unittest
from unittest.mock import patch
from scrapegraph_py.scrape import scrape

class TestScrape(unittest.TestCase):
    
    @patch('scrapegraph_py.scrape.requests.post')
    def test_scrape_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = '{"data": "extracted data"}'
        response = scrape("test_api_key", "http://example.com", "Extract data")
        self.assertEqual(response, '{"data": "extracted data"}')

    @patch('scrapegraph_py.scrape.requests.post')
    def test_scrape_http_error(self, mock_post):
        mock_post.side_effect = requests.exceptions.HTTPError
        response = scrape("test_api_key", "http://example.com", "Extract data")
        self.assertIn("HTTP error occurred", response)


if __name__ == '__main__':
    unittest.main() 