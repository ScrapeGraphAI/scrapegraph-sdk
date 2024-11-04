from pydantic import BaseModel, Field
from scrapegraph_py.scrape import scrape
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Define a Pydantic schema
class CompanyInfoSchema(BaseModel):
    company_name: str = Field(description="The name of the company")
    description: str = Field(description="A description of the company")
    main_products: list[str] = Field(description="The main products of the company")

# Example usage
api_key = os.getenv("SCRAPEGRAPH_API_KEY")
url = "https://scrapegraphai.com/"
prompt = "What does the company do?"

# Call the scrape function with the schema
result = scrape(api_key=api_key, url=url, prompt=prompt, schema=CompanyInfoSchema)

print(result)
