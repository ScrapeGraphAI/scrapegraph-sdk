import pytest
from scrapegraph_py.models.markdownify import MarkdownifyRequest, GetMarkdownifyRequest

def test_markdownify_request_invalid_url_scheme():
    """
    Test that MarkdownifyRequest raises a ValueError when the website_url does not
    start with either 'http://' or 'https://'.
    """
    with pytest.raises(ValueError, match="Invalid URL"):
        MarkdownifyRequest(website_url="ftp://example.com")

def test_markdownify_request_empty_url():
    """
    Test that MarkdownifyRequest raises a ValueError when the website_url is empty or contains only whitespace.
    """
    with pytest.raises(ValueError, match="Website URL cannot be empty"):
        MarkdownifyRequest(website_url="   ")

def test_markdownify_request_valid_url():
    """
    Test that MarkdownifyRequest properly creates an instance when provided with a valid URL.
    This covers the scenario where the input URL meets all validation requirements.
    """
    valid_url = "https://example.com"
    req = MarkdownifyRequest(website_url=valid_url)
    assert req.website_url == valid_url

def test_markdownify_request_untrimmed_url():
    """
    Test that MarkdownifyRequest raises a ValueError when the website_url contains leading or trailing whitespace.
    Although the stripped URL would be valid, the actual value is not processed further, causing the check
    for the proper URL scheme to fail.
    """
    # The URL has leading whitespace, so it does not start directly with "https://"
    with pytest.raises(ValueError, match="Invalid URL"):
        MarkdownifyRequest(website_url="   https://example.com")

def test_get_markdownify_request_invalid_uuid():
    """
    Test that GetMarkdownifyRequest raises a ValueError when the request_id is not a valid UUID.
    """
    with pytest.raises(ValueError, match="request_id must be a valid UUID"):
        GetMarkdownifyRequest(request_id="invalid_uuid")

def test_get_markdownify_request_valid_uuid():
    """
    Test that GetMarkdownifyRequest properly creates an instance when provided with a valid UUID.
    """
    valid_uuid = "123e4567-e89b-12d3-a456-426614174000"
    req = GetMarkdownifyRequest(request_id=valid_uuid)
    assert req.request_id == valid_uuid

def test_get_markdownify_request_untrimmed_uuid():
    """
    Test that GetMarkdownifyRequest raises a ValueError when the request_id
    contains leading or trailing whitespace, despite the trimmed UUID being valid.
    """
    with pytest.raises(ValueError, match="request_id must be a valid UUID"):
        GetMarkdownifyRequest(request_id=" 123e4567-e89b-12d3-a456-426614174000 ")
