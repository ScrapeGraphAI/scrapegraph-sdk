"""
Tests for crawl endpoint with path filtering functionality.
"""
import pytest
from scrapegraph_py.models.crawl import CrawlRequest


def test_crawl_request_with_include_paths():
    """Test CrawlRequest with include_paths"""
    request = CrawlRequest(
        url="https://example.com",
        prompt="Extract data",
        data_schema={"type": "object"},
        include_paths=["/products/*", "/blog/**"]
    )

    assert request.url == "https://example.com"
    assert request.include_paths == ["/products/*", "/blog/**"]
    assert request.exclude_paths is None


def test_crawl_request_with_exclude_paths():
    """Test CrawlRequest with exclude_paths"""
    request = CrawlRequest(
        url="https://example.com",
        prompt="Extract data",
        data_schema={"type": "object"},
        exclude_paths=["/admin/*", "/api/**"]
    )

    assert request.url == "https://example.com"
    assert request.exclude_paths == ["/admin/*", "/api/**"]
    assert request.include_paths is None


def test_crawl_request_with_both_path_filters():
    """Test CrawlRequest with both include and exclude paths"""
    request = CrawlRequest(
        url="https://example.com",
        prompt="Extract data",
        data_schema={"type": "object"},
        include_paths=["/products/**"],
        exclude_paths=["/products/archived/*"]
    )

    assert request.include_paths == ["/products/**"]
    assert request.exclude_paths == ["/products/archived/*"]


def test_crawl_request_invalid_include_path():
    """Test that include_paths must start with /"""
    with pytest.raises(ValueError, match="Include path must start with '/'"):
        CrawlRequest(
            url="https://example.com",
            prompt="Extract data",
            data_schema={"type": "object"},
            include_paths=["products/*"]  # Missing leading /
        )


def test_crawl_request_invalid_exclude_path():
    """Test that exclude_paths must start with /"""
    with pytest.raises(ValueError, match="Exclude path must start with '/'"):
        CrawlRequest(
            url="https://example.com",
            prompt="Extract data",
            data_schema={"type": "object"},
            exclude_paths=["admin/*"]  # Missing leading /
        )


def test_crawl_request_markdown_mode_with_paths():
    """Test CrawlRequest in markdown mode with path filtering"""
    request = CrawlRequest(
        url="https://example.com",
        extraction_mode=False,  # Markdown mode
        include_paths=["/blog/*"],
        exclude_paths=["/blog/drafts/*"]
    )

    assert request.extraction_mode is False
    assert request.include_paths == ["/blog/*"]
    assert request.exclude_paths == ["/blog/drafts/*"]


def test_crawl_request_serialization_excludes_none():
    """Test that None values are excluded from serialization"""
    request = CrawlRequest(
        url="https://example.com",
        prompt="Extract data",
        data_schema={"type": "object"}
        # include_paths and exclude_paths not provided (None)
    )

    serialized = request.model_dump(exclude_none=True)

    assert "include_paths" not in serialized
    assert "exclude_paths" not in serialized


def test_crawl_request_serialization_includes_paths():
    """Test that path filters are included in serialization when provided"""
    request = CrawlRequest(
        url="https://example.com",
        prompt="Extract data",
        data_schema={"type": "object"},
        include_paths=["/products/*"],
        exclude_paths=["/admin/*"]
    )

    serialized = request.model_dump(exclude_none=True)

    assert "include_paths" in serialized
    assert "exclude_paths" in serialized
    assert serialized["include_paths"] == ["/products/*"]
    assert serialized["exclude_paths"] == ["/admin/*"]
