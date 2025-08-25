#!/usr/bin/env python3
"""
Example script demonstrating the Generate Schema API endpoint using ScrapeGraph Python SDK.

This script shows how to:
1. Generate a new JSON schema from a search query
2. Modify an existing schema
3. Handle different types of search queries
4. Check the status of schema generation requests

Requirements:
- Python 3.7+
- scrapegraph-py package
- A .env file with your SGAI_API_KEY

Example .env file:
SGAI_API_KEY=your_api_key_here

Usage:
    python generate_schema_example.py
"""

import json
import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv

from scrapegraph_py import Client

# Load environment variables from .env file
load_dotenv()


class GenerateSchemaExample:
    """Example class for demonstrating the Generate Schema API using ScrapeGraph SDK"""

    def __init__(self, base_url: str = None, api_key: str = None):
        # Get API key from environment if not provided
        self.api_key = api_key or os.getenv("SGAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key must be provided or set in .env file as SGAI_API_KEY. "
                "Create a .env file with: SGAI_API_KEY=your_api_key_here"
            )
        
        # Initialize the ScrapeGraph client
        if base_url:
            # If base_url is provided, we'll need to modify the client to use it
            # For now, we'll use the default client and note the limitation
            print(f"⚠️  Note: Custom base_url {base_url} not yet supported in this example")
        
        self.client = Client(api_key=self.api_key)

    def print_schema_response(
        self, response: Dict[str, Any], title: str = "Schema Generation Response"
    ):
        """Pretty print the schema generation response"""
        print(f"\n{'='*60}")
        print(f" {title}")
        print(f"{'='*60}")

        if "error" in response and response["error"]:
            print(f"❌ Error: {response['error']}")
            return

        print(f"✅ Request ID: {response.get('request_id', 'N/A')}")
        print(f"📊 Status: {response.get('status', 'N/A')}")
        print(f"🔍 User Prompt: {response.get('user_prompt', 'N/A')}")
        print(f"✨ Refined Prompt: {response.get('refined_prompt', 'N/A')}")

        if "generated_schema" in response:
            print(f"\n📋 Generated Schema:")
            print(json.dumps(response["generated_schema"], indent=2))

    def run_examples(self):
        """Run all the example scenarios"""
        print("🚀 Generate Schema API Examples using ScrapeGraph Python SDK")
        print("=" * 60)

        # Example 1: Generate schema for e-commerce products
        print("\n1️⃣ Example: E-commerce Product Search")
        ecommerce_prompt = "Find laptops with specifications like brand, processor, RAM, storage, and price"
        try:
            response = self.client.generate_schema(ecommerce_prompt)
            self.print_schema_response(response, "E-commerce Products Schema")
        except Exception as e:
            print(f"❌ Error in e-commerce example: {e}")

        # Example 2: Generate schema for job listings
        print("\n2️⃣ Example: Job Listings Search")
        job_prompt = "Search for software engineering jobs with company name, position, location, salary range, and requirements"
        try:
            response = self.client.generate_schema(job_prompt)
            self.print_schema_response(response, "Job Listings Schema")
        except Exception as e:
            print(f"❌ Error in job listings example: {e}")

        # Example 3: Generate schema for news articles
        print("\n3️⃣ Example: News Articles Search")
        news_prompt = "Find technology news articles with headline, author, publication date, category, and summary"
        try:
            response = self.client.generate_schema(news_prompt)
            self.print_schema_response(response, "News Articles Schema")
        except Exception as e:
            print(f"❌ Error in news articles example: {e}")

        # Example 4: Modify existing schema
        print("\n4️⃣ Example: Modify Existing Schema")
        existing_schema = {
            "$defs": {
                "ProductSchema": {
                    "title": "ProductSchema",
                    "type": "object",
                    "properties": {
                        "name": {"title": "Name", "type": "string"},
                        "price": {"title": "Price", "type": "number"},
                    },
                    "required": ["name", "price"],
                }
            },
            "title": "ProductList",
            "type": "object",
            "properties": {
                "products": {
                    "title": "Products",
                    "type": "array",
                    "items": {"$ref": "#/$defs/ProductSchema"},
                }
            },
            "required": ["products"],
        }

        modification_prompt = (
            "Add brand, category, and rating fields to the existing product schema"
        )
        try:
            response = self.client.generate_schema(modification_prompt, existing_schema)
            self.print_schema_response(response, "Modified Product Schema")
        except Exception as e:
            print(f"❌ Error in schema modification example: {e}")

        # Example 5: Complex nested schema
        print("\n5️⃣ Example: Complex Nested Schema")
        complex_prompt = "Create a schema for a company directory with departments, each containing employees with contact info and projects"
        try:
            response = self.client.generate_schema(complex_prompt)
            self.print_schema_response(response, "Company Directory Schema")
        except Exception as e:
            print(f"❌ Error in complex schema example: {e}")

    def demonstrate_status_checking(self):
        """Demonstrate how to check the status of schema generation requests"""
        print("\n🔄 Demonstrating Status Checking...")
        
        # Generate a simple schema first
        prompt = "Find restaurants with name, cuisine, rating, and address"
        try:
            response = self.client.generate_schema(prompt)
            request_id = response.get('request_id')
            
            if request_id:
                print(f"📝 Generated schema request with ID: {request_id}")
                
                # Check the status
                print("🔍 Checking status...")
                status_response = self.client.get_schema_status(request_id)
                self.print_schema_response(status_response, f"Status Check for {request_id}")
            else:
                print("⚠️  No request ID returned from schema generation")
                
        except Exception as e:
            print(f"❌ Error in status checking demonstration: {e}")

    def close(self):
        """Close the client to free up resources"""
        if hasattr(self, 'client'):
            self.client.close()


def main():
    """Main function to run the examples"""
    # Check if API key is available
    if not os.getenv("SGAI_API_KEY"):
        print("Error: SGAI_API_KEY not found in .env file")
        print("Please create a .env file with your API key:")
        print("SGAI_API_KEY=your_api_key_here")
        return

    # Initialize the example class
    example = GenerateSchemaExample()

    try:
        # Run synchronous examples
        example.run_examples()

        # Demonstrate status checking
        example.demonstrate_status_checking()

    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
    finally:
        # Always close the client
        example.close()


if __name__ == "__main__":
    main()
