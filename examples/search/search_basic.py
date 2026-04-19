from dotenv import load_dotenv
load_dotenv()

from scrapegraph_py import ScrapeGraphAI, SearchRequest

sgai = ScrapeGraphAI()

res = sgai.search(SearchRequest(
    query="best programming languages 2024",
    num_results=3,
))

if res.status == "success":
    for result in res.data.results:
        print(f"\n{result.title}")
        print(f"URL: {result.url}")
        print(f"Content: {result.content[:200]}...")
else:
    print("Failed:", res.error)
