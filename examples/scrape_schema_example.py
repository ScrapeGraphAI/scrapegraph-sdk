from pydantic import BaseModel
from scrapegraphaiapisdk.scrape import scrape
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Define a Pydantic schema
class CompanyInfoSchema(BaseModel):
    company_name: str
    description: str
    main_products: list[str]

# Example usage
api_key = os.getenv("SCRAPEGRAPH_API_KEY")
url = "https://scrapegraphai.com/"
prompt = "What does the company do?"

# Create an instance of the schema with initial values
schema = CompanyInfoSchema(
    company_name="Example Company",
    description="An example company description.",
    main_products=["Product1", "Product2"]
)

# Call the scrape function with the schema
result = scrape(api_key=api_key, url=url, prompt=prompt, schema=schema)

print(result)
