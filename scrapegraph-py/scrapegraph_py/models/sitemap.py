"""Models for sitemap endpoint"""

from typing import Optional

from pydantic import BaseModel, Field, model_validator


class SitemapRequest(BaseModel):
    """Request model for sitemap endpoint.

    Extracts all URLs from a website's sitemap. Automatically discovers sitemap
    from robots.txt or common sitemap locations like /sitemap.xml and sitemap
    index files.

    The sitemap endpoint is useful for:
    - Discovering all pages on a website
    - Building comprehensive crawling lists
    - SEO audits and analysis
    - Content inventory management

    Attributes:
        website_url (str): The base URL of the website to extract sitemap from.
            Must start with http:// or https://. The API will automatically
            discover the sitemap location.
        mock (bool): Whether to use mock mode for the request. When True, returns
            stubbed responses without making actual API calls. Defaults to False.

    Raises:
        ValueError: If website_url is empty, None, or doesn't start with
            http:// or https://.

    Examples:
        Basic usage::

            >>> request = SitemapRequest(website_url="https://example.com")
            >>> print(request.website_url)
            https://example.com

        With mock mode::

            >>> request = SitemapRequest(
            ...     website_url="https://example.com",
            ...     mock=True
            ... )
            >>> print(request.mock)
            True

        The API automatically discovers sitemaps from:
        - robots.txt directives (Sitemap: https://example.com/sitemap.xml)
        - Common locations (/sitemap.xml, /sitemap_index.xml)
        - Sitemap index files with nested sitemaps

    Note:
        The website_url should be the base domain URL. The API will handle
        sitemap discovery automatically.
    """

    website_url: str = Field(
        ...,
        example="https://scrapegraphai.com/",
        description="The URL of the website to extract sitemap from"
    )
    mock: bool = Field(
        default=False,
        description="Whether to use mock mode for the request"
    )

    @model_validator(mode="after")
    def validate_url(self) -> "SitemapRequest":
        """Validate the website URL.

        Ensures the URL is not empty and uses http:// or https:// protocol.

        Returns:
            SitemapRequest: The validated instance.

        Raises:
            ValueError: If URL is empty or uses invalid protocol.
        """
        if self.website_url is None or not self.website_url.strip():
            raise ValueError("Website URL cannot be empty")
        if not (
            self.website_url.startswith("http://")
            or self.website_url.startswith("https://")
        ):
            raise ValueError("URL must start with http:// or https://")
        return self

    def model_dump(self, *args, **kwargs) -> dict:
        """Serialize the model to a dictionary.

        Automatically excludes None values from the serialized output to
        produce cleaner JSON payloads for the API.

        Args:
            *args: Positional arguments passed to parent model_dump.
            **kwargs: Keyword arguments passed to parent model_dump.
                If 'exclude_none' is not specified, it defaults to True.

        Returns:
            dict: Dictionary representation of the model with None values excluded.

        Examples:
            >>> request = SitemapRequest(website_url="https://example.com")
            >>> data = request.model_dump()
            >>> print(data)
            {'website_url': 'https://example.com', 'mock': False}
        """
        kwargs.setdefault("exclude_none", True)
        return super().model_dump(*args, **kwargs)


class SitemapResponse(BaseModel):
    """Response model for sitemap endpoint.

    Contains the complete list of URLs extracted from the website's sitemap.
    The URLs are returned in the order they appear in the sitemap, which
    typically reflects the website's intended structure and priority.

    This response is useful for:
    - Building comprehensive URL lists for crawling
    - Identifying content structure and organization
    - Discovering all public pages on a website
    - Planning content migration or archival

    Attributes:
        urls (list[str]): Complete list of URLs extracted from the sitemap.
            Each URL is a fully-qualified absolute URL string. The list may
            be empty if no sitemap is found or if the sitemap contains no URLs.
            URLs are deduplicated and ordered as they appear in the sitemap.

    Examples:
        Basic usage::

            >>> response = SitemapResponse(urls=[
            ...     "https://example.com/",
            ...     "https://example.com/about"
            ... ])
            >>> print(f"Found {len(response.urls)} URLs")
            Found 2 URLs

        Iterating over URLs::

            >>> response = SitemapResponse(urls=[
            ...     "https://example.com/",
            ...     "https://example.com/products",
            ...     "https://example.com/contact"
            ... ])
            >>> for url in response.urls:
            ...     print(url)
            https://example.com/
            https://example.com/products
            https://example.com/contact

        Filtering URLs::

            >>> response = SitemapResponse(urls=[
            ...     "https://example.com/",
            ...     "https://example.com/blog/post-1",
            ...     "https://example.com/blog/post-2",
            ...     "https://example.com/products"
            ... ])
            >>> blog_urls = [url for url in response.urls if '/blog/' in url]
            >>> print(f"Found {len(blog_urls)} blog posts")
            Found 2 blog posts

        Empty sitemap::

            >>> response = SitemapResponse(urls=[])
            >>> if not response.urls:
            ...     print("No URLs found in sitemap")
            No URLs found in sitemap

    Note:
        The urls list may contain various types of pages including:
        - Homepage and main sections
        - Blog posts and articles
        - Product pages
        - Category and tag pages
        - Media files (images, PDFs) if included in sitemap
    """

    urls: list[str] = Field(
        ...,
        description="List of URLs extracted from the sitemap",
        example=[
            "https://example.com/",
            "https://example.com/about",
            "https://example.com/products",
            "https://example.com/contact"
        ]
    )
