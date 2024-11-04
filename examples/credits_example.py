"""
This script demonstrates how to use the credits function from the credits module
to retrieve credits from the ScrapeGraph AI API.
"""

import os
from dotenv import load_dotenv
from scrapegraph_py.credits import credits

# Load environment variables from a .env file
load_dotenv()

def main():
    api_key = os.getenv("SCRAPEGRAPH_API_KEY")

    response = credits(api_key)
    print("Response from the API:")
    print(response)

if __name__ == "__main__":
    main() 