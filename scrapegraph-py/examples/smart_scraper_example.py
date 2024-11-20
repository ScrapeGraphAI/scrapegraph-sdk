import os
from scrapegraph_py import ScrapeGraphClient, smart_scraper
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SCRAPEGRAPH_API_KEY")
client = ScrapeGraphClient(api_key)

url = "https://scrapegraphai.com/"
prompt = "What does the company do?"

result = smart_scraper(client, url, prompt)
print(result)
