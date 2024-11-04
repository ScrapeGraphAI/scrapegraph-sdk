from scrapegraph_py.scrape import scrape
from dotenv import load_dotenv  # Import load_dotenv
import os  # Import os to access environment variables
import json  # Import json for beautifying output

def main():
    """Main function to execute the scraping process."""
    load_dotenv()
    api_key = os.getenv("SCRAPEGRAPH_API_KEY")
    url = "https://scrapegraphai.com/"
    prompt = "What does the company do?"

    result = scrape(api_key, url, prompt)
    print(result)
if __name__ == "__main__":
    main()
