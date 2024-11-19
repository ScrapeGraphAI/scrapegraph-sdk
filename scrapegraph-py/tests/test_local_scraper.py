import unittest
from unittest.mock import patch
from scrapegraph_py.local_scraper import scrape_text
from scrapegraph_py.client import ScrapeGraphClient
from pydantic import BaseModel, Field
import requests

class TestSchema(BaseModel):
    title: str = Field(description="The title")
    content: str = Field(description="The content")

class TestLocalScraper(unittest.TestCase):
    
    def setUp(self):
        self.client = ScrapeGraphClient("test_api_key")
    
    @patch('scrapegraph_py.local_scraper.requests.post')
    def test_scrape_text_success(self, mock_post):
        # Setup mock response
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = '{"title": "Test", "content": "Content"}'
        
        # Test basic scraping without schema
        response = scrape_text(
            self.client,
            "Sample website text",
            "Extract information"
        )
        self.assertEqual(response, '{"title": "Test", "content": "Content"}')

    @patch('scrapegraph_py.local_scraper.requests.post')
    def test_scrape_text_with_schema(self, mock_post):
        # Setup mock response
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = '{"title": "Test", "content": "Content"}'
        
        # Test scraping with schema
        response = scrape_text(
            self.client,
            "Sample website text",
            "Extract information",
            schema=TestSchema
        )
        self.assertEqual(response, '{"title": "Test", "content": "Content"}')

    @patch('scrapegraph_py.local_scraper.requests.post')
    def test_scrape_text_http_error(self, mock_post):
        # Test HTTP error handling
        mock_post.side_effect = requests.exceptions.HTTPError("404 Client Error")
        response = scrape_text(
            self.client,
            "Sample website text",
            "Extract information"
        )
        self.assertIn("HTTP error occurred", response)

    @patch('scrapegraph_py.local_scraper.requests.post')
    def test_scrape_text_forbidden(self, mock_post):
        # Test 403 forbidden error
        mock_response = mock_post.return_value
        mock_response.status_code = 403
        mock_post.side_effect = requests.exceptions.HTTPError("403 Forbidden")
        
        response = scrape_text(
            self.client,
            "Sample website text",
            "Extract information"
        )
        self.assertIn("Access forbidden (403)", response)

    @patch('scrapegraph_py.local_scraper.requests.post')
    def test_scrape_text_general_error(self, mock_post):
        # Test general request exception handling
        mock_post.side_effect = requests.exceptions.RequestException("Connection error")
        response = scrape_text(
            self.client,
            "Sample website text",
            "Extract information"
        )
        self.assertIn("An error occurred", response)

if __name__ == '__main__':
    unittest.main()
