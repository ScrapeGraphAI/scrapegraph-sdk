import pytest
from pydantic import BaseModel, ValidationError
from scrapegraph_py.models.smartscraper import SmartScraperRequest, GetSmartScraperRequest

# Define a dummy schema to test the output_schema conversion in model_dump
class DummySchema(BaseModel):
    """A dummy schema to simulate a Pydantic model with JSON schema conversion."""
    a: int = 1

def test_model_dump_with_output_schema_conversion():
    """
    Test that model_dump on SmartScraperRequest converts the provided output_schema into a JSON schema dict.
    """
    # Create a request with a valid user prompt, website URL, and a dummy output_schema.
    request = SmartScraperRequest(
        user_prompt="Extract information about the company",
        website_url="https://scrapegraphai.com/",
        output_schema=DummySchema
    )
    # Get the dump dict from the model.
    output = request.model_dump()
    # The model_dump should include the 'output_schema' converted to its JSON schema representation.
    expected_schema = DummySchema.model_json_schema()
    assert output.get("output_schema") == expected_schema

def test_model_dump_without_output_schema():
    """
    Test that model_dump on SmartScraperRequest returns output_schema as None 
    when no output_schema is provided. This ensures that the conversion logic is only 
    applied when output_schema is not None.
    """
    # Create a valid SmartScraperRequest without providing an output_schema.
    request = SmartScraperRequest(
        user_prompt="Extract some meaningful data",
        website_url="https://scrapegraphai.com/"
    )
    # Get the dumped dictionary from the model.
    output = request.model_dump()
    # Ensure that the output contains the key "output_schema" and its value is None.
    assert "output_schema" in output, "Output schema key should be present even if None"
    assert output["output_schema"] is None, "Output schema should be None when not provided"

def test_invalid_get_smartscraper_request_id():
    """
    Test that GetSmartScraperRequest raises a ValueError when provided with an invalid UUID.
    This test ensures that the request_id field is validated correctly.
    """
    with pytest.raises(ValueError, match="request_id must be a valid UUID"):
        GetSmartScraperRequest(request_id="invalid-uuid")


def test_smartscraper_request_with_pagination():
    """
    Test SmartScraperRequest with pagination parameter.
    This test ensures that the total_pages field is properly handled.
    """
    # Test with valid pagination
    request = SmartScraperRequest(
        user_prompt="Extract product information",
        website_url="https://example.com/products",
        total_pages=5
    )
    
    assert request.total_pages == 5
    
    # Test model_dump includes pagination
    output = request.model_dump()
    assert output["total_pages"] == 5
    
    # Test without pagination (default behavior)
    request_no_pagination = SmartScraperRequest(
        user_prompt="Extract product information",
        website_url="https://example.com/products"
    )
    
    assert request_no_pagination.total_pages is None
    
    # Test model_dump excludes None pagination
    output_no_pagination = request_no_pagination.model_dump()
    assert "total_pages" not in output_no_pagination


def test_smartscraper_request_pagination_validation():
    """
    Test pagination validation constraints.
    This test ensures that total_pages is properly validated.
    """
    # Test minimum value
    request = SmartScraperRequest(
        user_prompt="Extract products",
        website_url="https://example.com/products",
        total_pages=1
    )
    assert request.total_pages == 1
    
    # Test maximum value
    request = SmartScraperRequest(
        user_prompt="Extract products",
        website_url="https://example.com/products",
        total_pages=10
    )
    assert request.total_pages == 10
    
    # Test invalid values
    with pytest.raises(ValidationError):
        SmartScraperRequest(
            user_prompt="Extract products",
            website_url="https://example.com/products",
            total_pages=0
        )
    
    with pytest.raises(ValidationError):
        SmartScraperRequest(
            user_prompt="Extract products",
            website_url="https://example.com/products",
            total_pages=11
        )


def test_smartscraper_request_pagination_with_all_features():
    """
    Test pagination combined with other SmartScraper features.
    This test ensures pagination works with output_schema, scrolls, and headers.
    """
    headers = {"User-Agent": "test-agent"}
    
    request = SmartScraperRequest(
        user_prompt="Extract all product information",
        website_url="https://example.com/products",
        headers=headers,
        output_schema=DummySchema,
        number_of_scrolls=5,
        total_pages=3
    )
    
    assert request.total_pages == 3
    assert request.number_of_scrolls == 5
    assert request.headers == headers
    assert request.output_schema == DummySchema
    
    # Test model_dump with all features
    output = request.model_dump()
    assert output["total_pages"] == 3
    assert output["number_of_scrolls"] == 5
    assert output["headers"] == headers
    assert isinstance(output["output_schema"], dict)

def test_invalid_url_in_smartscraper_request():
    """
    Test that SmartScraperRequest raises a ValueError when provided with a website_url
    that does not start with 'http://' or 'https://'. This ensures the URL validation works.
    """
    with pytest.raises(ValueError, match="Invalid URL"):
        SmartScraperRequest(
            user_prompt="Extract data",
            website_url="ftp://invalid-url"
        )

def test_invalid_user_prompt_empty_and_non_alnum():
    """
    Test that SmartScraperRequest raises a ValueError when the user_prompt is either empty (or only whitespace)
    or when it contains no alphanumeric characters. This ensures the user prompt validator is working correctly.
    """
    # Test with a user_prompt that is empty (only whitespace)
    with pytest.raises(ValueError, match="User prompt cannot be empty"):
        SmartScraperRequest(
            user_prompt="   ",
            website_url="https://scrapegraphai.com/"
        )
    # Test with a user_prompt that contains no alphanumeric characters
    with pytest.raises(ValueError, match="User prompt must contain a valid prompt"):
        SmartScraperRequest(
            user_prompt="!!!",
            website_url="https://scrapegraphai.com/"
        )
