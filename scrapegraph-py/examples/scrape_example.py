import os
from scrapegraph_py import ScrapeGraphClient, scrape
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SCRAPEGRAPH_API_KEY")
client = ScrapeGraphClient(api_key)

url = "https://scrapegraphai.com/"
prompt = "What does the company do?"

result = scrape(client, url, prompt)
print(result)
