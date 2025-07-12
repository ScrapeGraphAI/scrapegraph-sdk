"""
Example demonstrating how to use the ScrapeGraphAI /v1/crawl/ API endpoint with a custom schema.

Requirements:
- Python 3.7+
- scrapegraph-py
- A .env file with your SGAI_API_KEY

Example .env file:
SGAI_API_KEY=your_api_key_here
"""

import json
import os
import time
from typing import Dict, Any, List, Optional

from dotenv import load_dotenv

from pydantic import BaseModel, EmailStr, HttpUrl
from scrapegraph_py import Client

# Load environment variables from .env file
load_dotenv()

# Pydantic models for schema
class SocialLinks(BaseModel):
    github: Optional[HttpUrl]
    linkedin: Optional[HttpUrl]
    twitter: Optional[HttpUrl]

class Company(BaseModel):
    name: str
    description: str
    features: Optional[List[str]] = None
    contact_email: Optional[EmailStr] = None
    social_links: Optional[SocialLinks] = None

class Service(BaseModel):
    service_name: str
    description: str
    features: Optional[List[str]] = None

class Legal(BaseModel):
    privacy_policy: str
    terms_of_service: str

class WebsiteContent(BaseModel):
    company: Company
    services: List[Service]
    legal: Legal

def main():
    if not os.getenv("SGAI_API_KEY"):
        print("Error: SGAI_API_KEY not found in .env file")
        print("Please create a .env file with your API key:")
        print("SGAI_API_KEY=your_api_key_here")
        return

    # Example schema (from your curl command)
    schema = WebsiteContent.schema()

    url = "https://scrapegraphai.com/"
    prompt = (
        "What does the company do? and I need text content from there privacy and terms"
    )

    try:
        # Initialize the client
        client = Client.from_env()

        # Start the crawl job
        print(f"\nStarting crawl for: {url}")
        start_time = time.time()
        crawl_response = client.crawl(
            url=url,
            prompt=prompt,
            data_schema=schema,
            cache_website=True,
            depth=2,
            max_pages=2,
            same_domain_only=True,
            batch_size=1,
        )
        execution_time = time.time() - start_time
        print(f"POST /v1/crawl/ execution time: {execution_time:.2f} seconds")
        print("\nCrawl job started. Response:")
        print(json.dumps(crawl_response, indent=2))

        # If the crawl is asynchronous and returns an ID, fetch the result
        crawl_id = crawl_response.get("id") or crawl_response.get("task_id")
        start_time = time.time()
        if crawl_id:
            print("\nPolling for crawl result...")
            for _ in range(10):
                time.sleep(5)
                result = client.get_crawl(crawl_id)
                if result.get("status") == "success" and result.get("result"):
                    execution_time = time.time() - start_time
                    print(
                        f"GET /v1/crawl/{crawl_id} execution time: {execution_time:.2f} seconds"
                    )
                    print("\nCrawl completed. Result:")
                    print(json.dumps(result["result"]["llm_result"], indent=2))
                    break
                elif result.get("status") == "failed":
                    print("\nCrawl failed. Result:")
                    print(json.dumps(result, indent=2))
                    break
                else:
                    print(f"Status: {result.get('status')}, waiting...")
            else:
                print("Crawl did not complete in time.")
        else:
            print("No crawl ID found in response. Synchronous result:")
            print(json.dumps(crawl_response, indent=2))

    except Exception as e:
        print(f"Error occurred: {str(e)}")


if __name__ == "__main__":
    main() 