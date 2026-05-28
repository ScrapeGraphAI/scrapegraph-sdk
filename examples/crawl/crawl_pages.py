import time

from dotenv import load_dotenv

from scrapegraph_py import ScrapeGraphAI, ScrapeMarkdownFormatEntry

load_dotenv()

sgai = ScrapeGraphAI()

start_res = sgai.crawl.start(
    "https://scrapegraphai.com/",
    max_pages=5,
    max_depth=2,
    formats=[ScrapeMarkdownFormatEntry()],
)

if start_res.status != "success" or not start_res.data:
    print("Failed to start:", start_res.error)
    raise SystemExit(1)

crawl_id = start_res.data.id
print("Crawl started:", crawl_id)

status = start_res.data.status
while status == "running":
    time.sleep(2)
    get_res = sgai.crawl.get(crawl_id)
    if get_res.status != "success" or not get_res.data:
        print("Failed to get status:", get_res.error)
        raise SystemExit(1)
    status = get_res.data.status
    print(f"Progress: {get_res.data.finished}/{get_res.data.total} - {status}")

cursor = 0
while True:
    pages_res = sgai.crawl.pages(crawl_id, cursor=cursor, limit=50)
    if pages_res.status != "success" or not pages_res.data:
        print("Failed to get pages:", pages_res.error)
        raise SystemExit(1)

    for page in pages_res.data.data:
        print(f"\nPage: {page.url}")
        print(f"Status: {page.status}")
        print(f"Title: {page.title}")

        markdown = (page.scrape.results.get("markdown") if page.scrape else None) or {}
        snippets = markdown.get("data") or []
        if snippets:
            print(snippets[0][:300])

    next_cursor = pages_res.data.pagination.next_cursor
    if next_cursor is None:
        break
    cursor = int(next_cursor)
