import os
from scrapegraph_py import scrape
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("SCRAPEGRAPH_API_KEY")
url = "https://scrapegraphai.com/"
prompt = "What does the company do?"

result = scrape(api_key, url, prompt)
print(result)
