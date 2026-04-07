"""
Integration test against the v2 dev API.

Run with:
    SGAI_API_KEY=... SGAI_API_BASE_URL=https://sgai-api-dev-v2.onrender.com/api/v1 \
        python -m pytest tests/test_integration_v2.py -v -m integration

Requires a valid API key and network access.
"""

import os

import pytest

from scrapegraph_py.client import Client

pytestmark = pytest.mark.integration

BASE_URL = os.getenv("SGAI_API_BASE_URL", "https://sgai-api-dev-v2.onrender.com/api/v1")


@pytest.fixture
def client():
    api_key = os.getenv("SGAI_API_KEY")
    if not api_key:
        pytest.skip("SGAI_API_KEY not set")

    # Patch the base URL for dev testing
    import scrapegraph_py.config as cfg

    original = cfg.API_BASE_URL
    cfg.API_BASE_URL = BASE_URL

    c = Client(api_key=api_key)
    yield c
    c.close()

    cfg.API_BASE_URL = original


def test_scrape_markdown(client):
    """Test scrape endpoint returns markdown for example.com."""
    result = client.scrape("https://example.com", format="markdown")
    print("\n=== Scrape result ===")
    print(result)
    assert result is not None


def test_scrape_html(client):
    """Test scrape endpoint returns HTML for example.com."""
    result = client.scrape("https://example.com", format="html")
    print("\n=== Scrape HTML result ===")
    print(result)
    assert result is not None
