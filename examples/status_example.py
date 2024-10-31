import os
from dotenv import load_dotenv
from scrapegraphaiapisdk.status import status

# Load environment variables from .env file
load_dotenv()

def main():
    # Get API key from environment variables
    api_key = os.getenv("SCRAPEGRAPH_API_KEY")
    
    # Check API status
    try:
        result = status(api_key)
        print(f"API Status: {result}")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main() 