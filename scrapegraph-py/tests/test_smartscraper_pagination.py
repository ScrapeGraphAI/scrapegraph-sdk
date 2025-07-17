import pytest
from pydantic import BaseModel, ValidationError
from scrapegraph_py.models.smartscraper import SmartScraperRequest, GetSmartScraperRequest


class TestProductSchema(BaseModel):
    """Test schema for pagination tests"""
    name: str
    price: str
    rating: float = None


class TestSmartScraperPagination:
    """Test suite for SmartScraper pagination functionality"""
    
    def test_smartscraper_request_with_pagination(self):
        """Test SmartScraperRequest with valid pagination parameters"""
        request = SmartScraperRequest(
            website_url="https://example.com/products",
            user_prompt="Extract product information",
            total_pages=5
        )
        
        assert request.website_url == "https://example.com/products"
        assert request.user_prompt == "Extract product information"
        assert request.total_pages == 5
        assert request.number_of_scrolls is None
        assert request.output_schema is None
        
    def test_smartscraper_request_with_pagination_and_schema(self):
        """Test SmartScraperRequest with pagination and output schema"""
        request = SmartScraperRequest(
            website_url="https://example.com/products",
            user_prompt="Extract product information",
            total_pages=3,
            output_schema=TestProductSchema
        )
        
        assert request.total_pages == 3
        assert request.output_schema == TestProductSchema
        
        # Test model_dump with pagination and schema
        dumped = request.model_dump()
        assert dumped["total_pages"] == 3
        assert isinstance(dumped["output_schema"], dict)
        assert "properties" in dumped["output_schema"]
        
    def test_smartscraper_request_with_pagination_and_scrolls(self):
        """Test SmartScraperRequest with both pagination and scrolling"""
        request = SmartScraperRequest(
            website_url="https://example.com/products",
            user_prompt="Extract product information",
            total_pages=2,
            number_of_scrolls=10
        )
        
        assert request.total_pages == 2
        assert request.number_of_scrolls == 10
        
        # Test model_dump excludes None values
        dumped = request.model_dump()
        assert dumped["total_pages"] == 2
        assert dumped["number_of_scrolls"] == 10
        assert "website_html" not in dumped  # Should be excluded since it's None
        
    def test_smartscraper_request_pagination_validation_minimum(self):
        """Test pagination validation - minimum value"""
        # Valid minimum value
        request = SmartScraperRequest(
            website_url="https://example.com/products",
            user_prompt="Extract product information",
            total_pages=1
        )
        assert request.total_pages == 1
        
        # Invalid minimum value (less than 1)
        with pytest.raises(ValidationError) as exc_info:
            SmartScraperRequest(
                website_url="https://example.com/products",
                user_prompt="Extract product information",
                total_pages=0
            )
        assert "greater than or equal to 1" in str(exc_info.value)
        
    def test_smartscraper_request_pagination_validation_maximum(self):
        """Test pagination validation - maximum value"""
        # Valid maximum value
        request = SmartScraperRequest(
            website_url="https://example.com/products",
            user_prompt="Extract product information",
            total_pages=10
        )
        assert request.total_pages == 10
        
        # Invalid maximum value (greater than 10)
        with pytest.raises(ValidationError) as exc_info:
            SmartScraperRequest(
                website_url="https://example.com/products",
                user_prompt="Extract product information",
                total_pages=11
            )
        assert "less than or equal to 10" in str(exc_info.value)
        
    def test_smartscraper_request_pagination_none_value(self):
        """Test SmartScraperRequest with None pagination (default behavior)"""
        request = SmartScraperRequest(
            website_url="https://example.com/products",
            user_prompt="Extract product information",
            total_pages=None
        )
        
        assert request.total_pages is None
        
        # Test model_dump excludes None values
        dumped = request.model_dump()
        assert "total_pages" not in dumped
        
    def test_smartscraper_request_pagination_with_html(self):
        """Test pagination with HTML content instead of URL"""
        html_content = """
        <html>
            <body>
                <div class="products">
                    <div class="product">Product 1</div>
                    <div class="product">Product 2</div>
                </div>
            </body>
        </html>
        """
        
        request = SmartScraperRequest(
            website_html=html_content,
            user_prompt="Extract product information",
            total_pages=2
        )
        
        assert request.website_html == html_content
        assert request.total_pages == 2
        assert request.website_url is None
        
    def test_smartscraper_request_pagination_with_headers(self):
        """Test pagination with custom headers"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Cookie": "session=abc123",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
        
        request = SmartScraperRequest(
            website_url="https://example.com/products",
            user_prompt="Extract product information",
            headers=headers,
            total_pages=3
        )
        
        assert request.headers == headers
        assert request.total_pages == 3
        
        # Test model_dump includes headers and pagination
        dumped = request.model_dump()
        assert dumped["headers"] == headers
        assert dumped["total_pages"] == 3
        
    def test_smartscraper_request_pagination_edge_cases(self):
        """Test edge cases for pagination"""
        # Test with negative value
        with pytest.raises(ValidationError):
            SmartScraperRequest(
                website_url="https://example.com/products",
                user_prompt="Extract product information",
                total_pages=-1
            )
        
        # Test with float value (should be converted to int or rejected)
        with pytest.raises(ValidationError):
            SmartScraperRequest(
                website_url="https://example.com/products",
                user_prompt="Extract product information",
                total_pages=2.5
            )
        
        # Test with string value
        with pytest.raises(ValidationError):
            SmartScraperRequest(
                website_url="https://example.com/products",
                user_prompt="Extract product information",
                total_pages="5"
            )
            
    def test_smartscraper_request_pagination_model_dump_exclude_none(self):
        """Test that model_dump properly excludes None values for pagination"""
        # Request with pagination
        request_with_pagination = SmartScraperRequest(
            website_url="https://example.com/products",
            user_prompt="Extract product information",
            total_pages=3
        )
        
        dumped_with_pagination = request_with_pagination.model_dump()
        assert "total_pages" in dumped_with_pagination
        assert dumped_with_pagination["total_pages"] == 3
        
        # Request without pagination
        request_without_pagination = SmartScraperRequest(
            website_url="https://example.com/products",
            user_prompt="Extract product information"
        )
        
        dumped_without_pagination = request_without_pagination.model_dump()
        assert "total_pages" not in dumped_without_pagination
        
    def test_smartscraper_request_pagination_with_all_parameters(self):
        """Test SmartScraperRequest with all parameters including pagination"""
        headers = {"User-Agent": "test-agent"}
        
        request = SmartScraperRequest(
            website_url="https://example.com/products",
            user_prompt="Extract all product information",
            headers=headers,
            output_schema=TestProductSchema,
            number_of_scrolls=5,
            total_pages=7
        )
        
        assert request.website_url == "https://example.com/products"
        assert request.user_prompt == "Extract all product information"
        assert request.headers == headers
        assert request.output_schema == TestProductSchema
        assert request.number_of_scrolls == 5
        assert request.total_pages == 7
        
        # Test model_dump with all parameters
        dumped = request.model_dump()
        assert dumped["website_url"] == "https://example.com/products"
        assert dumped["user_prompt"] == "Extract all product information"
        assert dumped["headers"] == headers
        assert isinstance(dumped["output_schema"], dict)
        assert dumped["number_of_scrolls"] == 5
        assert dumped["total_pages"] == 7
        
    def test_smartscraper_request_pagination_validation_with_existing_validators(self):
        """Test that pagination validation works alongside existing validators"""
        # Test empty prompt with pagination - should fail on prompt validation
        with pytest.raises(ValidationError) as exc_info:
            SmartScraperRequest(
                website_url="https://example.com/products",
                user_prompt="",
                total_pages=5
            )
        assert "User prompt cannot be empty" in str(exc_info.value)
        
        # Test invalid URL with pagination - should fail on URL validation
        with pytest.raises(ValidationError) as exc_info:
            SmartScraperRequest(
                website_url="invalid-url",
                user_prompt="Extract products",
                total_pages=3
            )
        assert "Invalid URL" in str(exc_info.value)
        
        # Test pagination with neither URL nor HTML - should fail on URL/HTML validation
        with pytest.raises(ValidationError) as exc_info:
            SmartScraperRequest(
                user_prompt="Extract products",
                total_pages=2
            )
        assert "Either website_url or website_html must be provided" in str(exc_info.value)
        
    def test_smartscraper_request_pagination_boundary_values(self):
        """Test pagination boundary values"""
        # Test boundary values
        valid_values = [1, 2, 5, 9, 10]
        
        for value in valid_values:
            request = SmartScraperRequest(
                website_url="https://example.com/products",
                user_prompt="Extract products",
                total_pages=value
            )
            assert request.total_pages == value
            
        # Test invalid boundary values
        invalid_values = [0, -1, 11, 100]
        
        for value in invalid_values:
            with pytest.raises(ValidationError):
                SmartScraperRequest(
                    website_url="https://example.com/products",
                    user_prompt="Extract products",
                    total_pages=value
                )
                
    def test_get_smartscraper_request_unchanged(self):
        """Test that GetSmartScraperRequest is not affected by pagination changes"""
        # This should still work as before
        request = GetSmartScraperRequest(request_id="123e4567-e89b-12d3-a456-426614174000")
        assert request.request_id == "123e4567-e89b-12d3-a456-426614174000"
        
        # Invalid UUID should still raise error
        with pytest.raises(ValidationError) as exc_info:
            GetSmartScraperRequest(request_id="invalid-uuid")
        assert "request_id must be a valid UUID" in str(exc_info.value) 