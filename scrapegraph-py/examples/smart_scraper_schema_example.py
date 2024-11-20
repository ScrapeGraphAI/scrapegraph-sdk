import os
from pydantic import BaseModel, Field
from scrapegraph_py import ScrapeGraphClient, smart_scraper
from dotenv import load_dotenv

load_dotenv()

# Define a Pydantic schema
class CompanyInfoSchema(BaseModel):
    company_name: str = Field(description="The name of the company")
    description: str = Field(description="A description of the company")
    main_products: list[str] = Field(description="The main products of the company")

# Initialize client
api_key = os.getenv("SCRAPEGRAPH_API_KEY")
client = ScrapeGraphClient(api_key)

url = "https://scrapegraphai.com/"
prompt = "What does the company do?"

# Call the scrape function with the schema
result = smart_scraper(client=client, url=url, prompt=prompt, schema=CompanyInfoSchema)
print(result)
