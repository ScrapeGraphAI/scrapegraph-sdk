from dotenv import load_dotenv
load_dotenv()

from scrapegraph_py import ScrapeGraphAI, ScrapeRequest, MarkdownFormatConfig

sgai = ScrapeGraphAI()

res = sgai.scrape(ScrapeRequest(
    url="https://example.com",
    formats=[MarkdownFormatConfig()],
))

if res.status == "success":
    print("Markdown:", res.data.results.get("markdown", {}).get("data"))
    print(f"\nTook {res.elapsed_ms}ms")
else:
    print("Failed:", res.error)
