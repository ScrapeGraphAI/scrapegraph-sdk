from bs4 import BeautifulSoup
import os

def scrape_local_html(file_path):
    """
    Scrape content from a local HTML file.
    
    Args:
        file_path (str): Path to the local HTML file
        
    Returns:
        dict: Extracted data from the HTML file
    """
    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"HTML file not found at: {file_path}")
    
    # Read the HTML file
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Example extraction - modify based on your HTML structure
    data = {
        'title': soup.title.string if soup.title else None,
        'paragraphs': [p.text for p in soup.find_all('p')],
        'links': [{'text': a.text, 'href': a.get('href')} for a in soup.find_all('a')],
        'headers': [h.text for h in soup.find_all(['h1', 'h2', 'h3'])]
    }
    
    return data

def main():
    # Example usage
    try:
        # Assuming you have a sample.html file in the same directory
        result = scrape_local_html('sample.html')
        
        # Print extracted data
        print("Title:", result['title'])
        print("\nParagraphs:")
        for p in result['paragraphs']:
            print(f"- {p}")
            
        print("\nLinks:")
        for link in result['links']:
            print(f"- {link['text']}: {link['href']}")
            
        print("\nHeaders:")
        for header in result['headers']:
            print(f"- {header}")
            
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
