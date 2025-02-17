import pytest
from pydantic import BaseModel
from scrapegraph_py.models.localscraper import LocalScraperRequest, GetLocalScraperRequest

# Create a dummy output schema to test the conversion in model_dump.
class DummySchema(BaseModel):
    test_field: str

def test_output_schema_conversion():
    """
    Test that when an output_schema is provided in a LocalScraperRequest,
    model_dump returns a dictionary where the output_schema key holds the JSON schema
    of the provided Pydantic model.
    """
    user_prompt = "Extract company details"
    website_html = "<html><body><div>Content</div></body></html>"
    # Create a LocalScraperRequest with a dummy output_schema.
    request = LocalScraperRequest(user_prompt=user_prompt, website_html=website_html, output_schema=DummySchema)
    dumped = request.model_dump()
    # Verify that output_schema is converted properly in the dumped dictionary.
    assert "output_schema" in dumped
    assert dumped["output_schema"] == DummySchema.model_json_schema()

def test_invalid_website_html_structure():
    """
    Test that LocalScraperRequest raises a ValueError when the website_html provided
    has no parseable HTML tags. This ensures the HTML content validation catches 
    non-HTML input.
    """
    # This string has no HTML tags so BeautifulSoup.find() should return None.
    invalid_html = "Just some random text"
    with pytest.raises(ValueError, match="Invalid HTML - no parseable content found"):
        LocalScraperRequest(user_prompt="Extract info about the company", website_html=invalid_html)

def test_invalid_user_prompt_non_alnum():
    """
    Test that LocalScraperRequest raises a ValueError when the user_prompt 
    does not contain any alphanumeric characters.
    """
    with pytest.raises(ValueError, match="User prompt must contain a valid prompt"):
        LocalScraperRequest(
            user_prompt="!!!",
            website_html="<html><body><div>Valid Content</div></body></html>"
        )

def test_get_localscraper_request_invalid_uuid():
    """
    Test that GetLocalScraperRequest raises a ValueError when an invalid UUID is provided.
    This ensures that the model correctly validates the request_id as a proper UUID.
    """
    invalid_uuid = "not-a-valid-uuid"
    with pytest.raises(ValueError, match="request_id must be a valid UUID"):
        GetLocalScraperRequest(request_id=invalid_uuid)

def test_website_html_exceeds_maximum_size():
    """
    Test that LocalScraperRequest raises a ValueError when the website_html content
    exceeds the maximum allowed size of 2MB. The generated HTML is valid but too large.
    """
    # Calculate the number of characters needed to exceed 2MB when encoded in UTF-8.
    max_size_bytes = 2 * 1024 * 1024
    # Create a valid HTML string that exceeds 2MB.
    base_html_prefix = "<html><body>"
    base_html_suffix = "</body></html>"
    repeated_char_length = max_size_bytes - len(base_html_prefix.encode("utf-8")) - len(base_html_suffix.encode("utf-8")) + 1
    oversized_content = "a" * repeated_char_length
    oversized_html = f"{base_html_prefix}{oversized_content}{base_html_suffix}"
    
    with pytest.raises(ValueError, match="Website HTML content exceeds maximum size of 2MB"):
        LocalScraperRequest(user_prompt="Extract info", website_html=oversized_html)

def test_website_html_exactly_maximum_size():
    """
    Test that LocalScraperRequest accepts website_html content exactly 2MB in size.
    This ensures that the size validation correctly allows content on the boundary.
    """
    user_prompt = "Extract info with exact size HTML"
    prefix = "<html><body>"
    suffix = "</body></html>"
    # Calculate the length of the content needed to exactly reach 2MB when combined with prefix and suffix.
    max_size_bytes = 2 * 1024 * 1024
    content_length = max_size_bytes - len(prefix.encode("utf-8")) - len(suffix.encode("utf-8"))
    valid_content = "a" * content_length
    html = prefix + valid_content + suffix
    
    # Attempt to create a valid LocalScraperRequest.
    request = LocalScraperRequest(user_prompt=user_prompt, website_html=html)
    
    # Verify that the HTML content is exactly 2MB in size when encoded in UTF-8.
    assert len(request.website_html.encode("utf-8")) == max_size_bytes
