import os

import pytest
from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("SGAI_API_KEY"):
    pytest.skip("SGAI_API_KEY env var required for integration tests", allow_module_level=True)

from scrapegraph_py import (
    CrawlRequest,
    ExtractRequest,
    FetchConfig,
    HistoryFilter,
    ImagesFormatConfig,
    LinksFormatConfig,
    MarkdownFormatConfig,
    ScrapeGraphAI,
    ScrapeRequest,
    SearchRequest,
)

sgai = ScrapeGraphAI()


class TestIntegration:
    def test_credits(self):
        res = sgai.credits()
        print("credits:", res)
        assert res.status == "success"
        assert "remaining" in res.data
        assert "plan" in res.data

    def test_scrape_default_format(self):
        res = sgai.scrape(ScrapeRequest(url="https://example.com"))
        print("scrape default:", res.status, res.error)
        assert res.status == "success"
        assert res.data["results"].get("markdown") is not None

    def test_scrape_single_format(self):
        res = sgai.scrape(
            ScrapeRequest(
                url="https://example.com",
                formats=[MarkdownFormatConfig()],
            )
        )
        print("scrape single:", res.status, res.error)
        assert res.status == "success"
        assert res.data["results"].get("markdown") is not None

    def test_scrape_multiple_formats(self):
        res = sgai.scrape(
            ScrapeRequest(
                url="https://example.com",
                formats=[
                    MarkdownFormatConfig(mode="reader"),
                    LinksFormatConfig(),
                    ImagesFormatConfig(),
                ],
            )
        )
        print("scrape multi:", res.status, res.error)
        assert res.status == "success"
        assert res.data["results"].get("markdown") is not None
        assert res.data["results"].get("links") is not None

    def test_scrape_pdf(self):
        res = sgai.scrape(
            ScrapeRequest(
                url="https://pdfobject.com/pdf/sample.pdf",
                content_type="application/pdf",
                formats=[MarkdownFormatConfig()],
            )
        )
        print("scrape PDF:", res.status, res.error)
        assert res.status == "success"
        assert res.data["metadata"]["contentType"] == "application/pdf"

    def test_scrape_with_fetch_config(self):
        res = sgai.scrape(
            ScrapeRequest(
                url="https://example.com",
                fetch_config=FetchConfig(mode="fast", timeout=15000),
                formats=[MarkdownFormatConfig()],
            )
        )
        print("scrape fetchConfig:", res.status, res.error)
        assert res.status == "success"

    def test_extract(self):
        res = sgai.extract(
            ExtractRequest(
                url="https://example.com",
                prompt="What is this page about?",
            )
        )
        print("extract:", res.status, res.error)
        assert res.status == "success"

    def test_search(self):
        res = sgai.search(
            SearchRequest(
                query="anthropic claude",
                num_results=2,
            )
        )
        print("search:", res.status, res.error)
        assert res.status == "success"
        assert len(res.data["results"]) > 0

    def test_history_list(self):
        res = sgai.history.list(HistoryFilter(limit=5))
        print("history.list:", res.status, res.data.get("pagination") if res.data else None)
        assert res.status == "success"

    def test_crawl_start_and_get(self):
        start_res = sgai.crawl.start(
            CrawlRequest(
                url="https://example.com",
                max_pages=2,
            )
        )
        print(
            "crawl.start:",
            start_res.status,
            start_res.data.get("id") if start_res.data else None,
            start_res.error,
        )

        if start_res.status == "error" and (
            "Max" in (start_res.error or "") or "Rate" in (start_res.error or "")
        ):
            pytest.skip("Rate limited")

        assert start_res.status == "success"

        if start_res.data and start_res.data.get("id"):
            get_res = sgai.crawl.get(start_res.data["id"])
            print(
                "crawl.get:", get_res.status, get_res.data.get("status") if get_res.data else None
            )
            assert get_res.status == "success"
