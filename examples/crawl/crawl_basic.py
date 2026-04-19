from dotenv import load_dotenv
load_dotenv()

import time
from scrapegraph_py import ScrapeGraphAI, CrawlRequest

sgai = ScrapeGraphAI()

start_res = sgai.crawl.start(CrawlRequest(
    url="https://scrapegraphai.com/",
    max_pages=5,
    max_depth=2,
))

if start_res.status != "success" or not start_res.data:
    print("Failed to start:", start_res.error)
else:
    crawl_id = start_res.data.id
    print("Crawl started:", crawl_id)

    status = start_res.data.status
    while status == "running":
        time.sleep(2)
        get_res = sgai.crawl.get(crawl_id)
        if get_res.status != "success" or not get_res.data:
            print("Failed to get status:", get_res.error)
            break
        status = get_res.data.status
        print(f"Progress: {get_res.data.finished}/{get_res.data.total} - {status}")

        if status in ("completed", "failed"):
            print("\nPages crawled:")
            for page in get_res.data.pages:
                print(f"  {page.url} - {page.status}")
