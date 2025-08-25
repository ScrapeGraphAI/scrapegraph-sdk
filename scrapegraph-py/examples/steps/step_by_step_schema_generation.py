#!/usr/bin/env python3
"""
Step-by-step example for schema generation using ScrapeGraph Python SDK.

This script demonstrates the basic workflow for schema generation:
1. Initialize the client
2. Generate a schema from a prompt
3. Check the status of the request
4. Retrieve the final result

Requirements:
- Python 3.7+
- scrapegraph-py package
- A .env file with your SGAI_API_KEY

Example .env file:
SGAI_API_KEY=your_api_key_here

Usage:
    python step_by_step_schema_generation.py
"""

import json
import os
import time
from typing import Any, Dict

from dotenv import load_dotenv

from scrapegraph_py import Client

# Load environment variables from .env file
load_dotenv()


def print_step(step_number: int, title: str, description: str = ""):
    """Print a formatted step header"""
    print(f"\n{'='*60}")
    print(f"STEP {step_number}: {title}")
    print(f"{'='*60}")
    if description:
        print(description)
    print()


def print_response(response: Dict[str, Any], title: str = "API Response"):
    """Pretty print an API response"""
    print(f"\n📋 {title}")
    print("-" * 40)
    
    if "error" in response and response["error"]:
        print(f"❌ Error: {response['error']}")
        return

    for key, value in response.items():
        if key == "generated_schema" and value:
            print(f"🔧 {key}:")
            print(json.dumps(value, indent=2))
        else:
            print(f"🔧 {key}: {value}")


def main():
    """Main function demonstrating step-by-step schema generation"""
    
    # Step 1: Check API key and initialize client
    print_step(1, "Initialize Client", "Setting up the ScrapeGraph client with your API key")
    
    api_key = os.getenv("SGAI_API_KEY")
    if not api_key:
        print("❌ Error: SGAI_API_KEY not found in .env file")
        print("Please create a .env file with your API key:")
        print("SGAI_API_KEY=your_api_key_here")
        return
    
    try:
        client = Client(api_key=api_key)
        print("✅ Client initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return

    # Step 2: Define the schema generation request
    print_step(2, "Define Request", "Creating a prompt for schema generation")
    
    user_prompt = "Find laptops with specifications like brand, processor, RAM, storage, and price"
    print(f"💭 User Prompt: {user_prompt}")
    
    # Step 3: Generate the schema
    print_step(3, "Generate Schema", "Sending the schema generation request to the API")
    
    try:
        response = client.generate_schema(user_prompt)
        print("✅ Schema generation request sent successfully")
        print_response(response, "Initial Response")
        
        # Extract the request ID for status checking
        request_id = response.get('request_id')
        if not request_id:
            print("❌ No request ID returned from the API")
            return
            
    except Exception as e:
        print(f"❌ Failed to generate schema: {e}")
        return

    # Step 4: Check the status (polling)
    print_step(4, "Check Status", "Polling the API to check the status of the request")
    
    max_attempts = 10
    attempt = 0
    
    while attempt < max_attempts:
        attempt += 1
        print(f"🔍 Attempt {attempt}/{max_attempts}: Checking status...")
        
        try:
            status_response = client.get_schema_status(request_id)
            current_status = status_response.get('status', 'unknown')
            
            print(f"📊 Current Status: {current_status}")
            
            if current_status == 'completed':
                print("✅ Schema generation completed successfully!")
                print_response(status_response, "Final Result")
                break
            elif current_status == 'failed':
                print("❌ Schema generation failed")
                print_response(status_response, "Error Response")
                break
            elif current_status in ['pending', 'processing']:
                print("⏳ Request is still being processed, waiting...")
                if attempt < max_attempts:
                    time.sleep(2)  # Wait 2 seconds before next check
            else:
                print(f"⚠️  Unknown status: {current_status}")
                break
                
        except Exception as e:
            print(f"❌ Error checking status: {e}")
            break
    
    if attempt >= max_attempts:
        print("⚠️  Maximum attempts reached. The request might still be processing.")
        print("You can check the status later using the request ID.")

    # Step 5: Demonstrate schema modification
    print_step(5, "Schema Modification", "Demonstrating how to modify an existing schema")
    
    existing_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "price": {"type": "number"},
        },
        "required": ["name", "price"],
    }
    
    modification_prompt = "Add brand and rating fields to the existing schema"
    print(f"💭 Modification Prompt: {modification_prompt}")
    print(f"📋 Existing Schema: {json.dumps(existing_schema, indent=2)}")
    
    try:
        modification_response = client.generate_schema(modification_prompt, existing_schema)
        print("✅ Schema modification request sent successfully")
        print_response(modification_response, "Modification Response")
        
    except Exception as e:
        print(f"❌ Failed to modify schema: {e}")

    # Step 6: Cleanup
    print_step(6, "Cleanup", "Closing the client to free up resources")
    
    try:
        client.close()
        print("✅ Client closed successfully")
    except Exception as e:
        print(f"⚠️  Warning: Error closing client: {e}")

    print("\n🎉 Schema generation demonstration completed!")
    print(f"📝 Request ID for reference: {request_id}")


if __name__ == "__main__":
    main()
