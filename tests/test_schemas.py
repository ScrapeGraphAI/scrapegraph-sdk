import pytest
from pydantic import ValidationError

from scrapegraph_py import (
    CrawlRequest,
    ExtractRequest,
    ScrapeRequest,
    SearchRequest,
)

REQUESTS = [
    (ScrapeRequest, {"url": "https://example.com"}),
    (ExtractRequest, {"url": "https://example.com", "prompt": "title"}),
    (SearchRequest, {"query": "example"}),
    (CrawlRequest, {"url": "https://example.com"}),
]


@pytest.mark.parametrize(("request_model", "base"), REQUESTS)
def test_documented_pdf_configuration(request_model, base):
    request = request_model(
        **base,
        allowed_types=["application/pdf"],
        processors=[{"type": "pdf", "max_pages": 10}],
    )

    assert request.model_dump(by_alias=True, mode="json", exclude_none=True)["processors"] == [
        {"type": "pdf", "maxPages": 10}
    ]


@pytest.mark.parametrize(("request_model", "base"), REQUESTS)
def test_default_pdf_cap_can_be_omitted(request_model, base):
    request = request_model(**base)
    assert "processors" not in request.model_dump(by_alias=True, mode="json", exclude_none=True)

    request = request_model(**base, processors=[{"type": "pdf"}])
    assert request.model_dump(by_alias=True, mode="json", exclude_none=True)["processors"] == [
        {"type": "pdf", "maxPages": 25}
    ]


@pytest.mark.parametrize(("request_model", "base"), REQUESTS)
@pytest.mark.parametrize(
    "invalid",
    [
        {"allowed_types": []},
        {"allowed_types": ["application/pdf", "application/pdf"]},
        {"processors": []},
        {
            "processors": [
                {"type": "pdf", "max_pages": 1},
                {"type": "pdf", "max_pages": 10},
            ]
        },
    ],
)
def test_rejects_empty_and_duplicate_arrays(request_model, base, invalid):
    with pytest.raises(ValidationError):
        request_model(**base, **invalid)


@pytest.mark.parametrize(("request_model", "base"), REQUESTS)
@pytest.mark.parametrize("max_pages", [1, 500, -1])
def test_accepts_documented_pdf_page_limits(request_model, base, max_pages):
    request_model(**base, processors=[{"type": "pdf", "max_pages": max_pages}])


@pytest.mark.parametrize(("request_model", "base"), REQUESTS)
@pytest.mark.parametrize("max_pages", [0, -2, 501, 1.5])
def test_rejects_invalid_pdf_page_limits(request_model, base, max_pages):
    with pytest.raises(ValidationError):
        request_model(**base, processors=[{"type": "pdf", "max_pages": max_pages}])
