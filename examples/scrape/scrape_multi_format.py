from dotenv import load_dotenv
load_dotenv()

from scrapegraph_py import (
    ScrapeGraphAI,
    ScrapeRequest,
    MarkdownFormatConfig,
    LinksFormatConfig,
    ScreenshotFormatConfig,
)

sgai = ScrapeGraphAI()

res = sgai.scrape(ScrapeRequest(
    url="https://example.com",
    formats=[
        MarkdownFormatConfig(),
        LinksFormatConfig(),
        ScreenshotFormatConfig(width=1280, height=720),
    ],
))

if res.status == "success":
    results = res.data.results

    print("=== Markdown ===")
    print(results.get("markdown", {}).get("data", [""])[0][:500], "...")

    print("\n=== Links ===")
    links = results.get("links", {}).get("data", [])
    print(f"Found {len(links)} links")
    for link in links[:5]:
        print(f"  - {link}")

    print("\n=== Screenshot ===")
    screenshot = results.get("screenshot", {}).get("data", {})
    print(f"URL: {screenshot.get('url')}")
    print(f"Size: {screenshot.get('width')}x{screenshot.get('height')}")
else:
    print("Failed:", res.error)
