from bs4 import BeautifulSoup
import os
from scrapegraph_py import ScrapeGraphClient, scrape_text
from dotenv import load_dotenv

def scrape_local_html(client: ScrapeGraphClient, file_path: str, prompt: str):
    """
    Scrape content from a local HTML file using ScrapeGraph AI.
    
    Args:
        client (ScrapeGraphClient): Initialized ScrapeGraph client
        file_path (str): Path to the local HTML file
        prompt (str): Natural language prompt describing what to extract
        
    Returns:
        str: Extracted data in JSON format
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"HTML file not found at: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Use BeautifulSoup to extract text content
    soup = BeautifulSoup(html_content, 'html.parser')
    text_content = soup.get_text(separator='\n', strip=True)
    
    # Use ScrapeGraph AI to analyze the text
    return scrape_text(client, text_content, prompt)

def main():
    load_dotenv()
    api_key = os.getenv("SCRAPEGRAPH_API_KEY")
    client = ScrapeGraphClient(api_key)
    
    try:
        result = scrape_local_html(
            client,
            'sample.html',
            "Extract main content and important information"
        )
        print("Extracted Data:", result)
            
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
